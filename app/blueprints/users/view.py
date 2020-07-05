from sanic import Blueprint
from sanic.request import Request
from sanic.response import json
from sanic_jwt.decorators import inject_user, protected
from sanic_openapi import doc  # pylint: disable=wrong-import-order

from app.helpers import loaders, validators
from app.helpers.swagger import models as swagger_models
from app.helpers.swagger.docs import json_consumes
from database import User, Assessment


blueprint = Blueprint('users', url_prefix='/users', strict_slashes=True)


@doc.summary('Получение пользователя')
@doc.security(True)
@doc.response(200, swagger_models.User)
@blueprint.get('/me')
@protected()
@inject_user()
async def get_user(request: Request, user: User):  # pylint: disable=unused-argument
    return json(user.to_dict())


@doc.summary('Получение количества оцененных фоток')
@doc.security(True)
@doc.response(200, doc.Dictionary({'count': doc.Integer()}))
@blueprint.get('/count_photos')
@protected()
@inject_user()
async def get_count_photo(request: Request, user: User):  # pylint: disable=unused-argument
    count = await Assessment.query.where(Assessment.user_id == user.id).gino.all()
    return json({'count': len(count)})


@doc.summary('Обновление пользователя')
@doc.security(True)
@json_consumes(
    {
        'login': swagger_models.User.login,
        'password': doc.String(User.password.comment),
    }
)
@doc.response(200, swagger_models.User)
@blueprint.put('/me')
@protected()
@inject_user()
async def update_user(request: Request, user: User):
    validators.raise_if_empty(request.json)

    login = request.json.get('login')
    password = request.json.get('password')

    user_update = None
    if login is not None:
        user_update = (user_update or user).update(login=login)
    if password:
        argon2 = request.app.argon2
        hashed_password = await argon2.async_hash(password)
        user_update = (user_update or user).update(password=hashed_password.encode('utf-8'))
    if user_update:
        await user_update.apply()

    return json(user.to_dict())
