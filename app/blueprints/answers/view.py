from typing import Optional
from sqlalchemy import or_, not_, and_, tuple_
from sanic import Blueprint
from sanic.request import Request
from sanic.response import json
from database import Photo, db, Assessment, User
from sqlalchemy.sql import func, exists
from app.helpers.swagger import models as swagger_models
from sanic_openapi import doc  # pylint: disable=wrong-import-order
from sanic_jwt.decorators import inject_user, protected
from app.helpers.validators import raise_if_empty, raise_if_not_int, raise_if_not_float
from app.helpers.loaders import admin_load_photos, load_photos, load_users

blueprint = Blueprint('photo', url_prefix='/photo', strict_slashes=True)


@doc.summary('Получение Фотографий')
@doc.security(True)
@doc.consumes({'offset': doc.Integer('Сдвиг')}, default_value=0)
@doc.consumes({'limit': doc.Integer('Количество')})
@doc.response(200, doc.List(swagger_models.Photo))
@blueprint.get('')
@protected()
@inject_user()
async def get_photos(request: Request, user: User):
    limit = request.args.get('limit')
    offset = request.args.get('offset', default=0)
    raise_if_empty(limit, offset)
    raise_if_not_int(limit, offset)
    if user.login == 'admin':
        photos_loads = admin_load_photos(limit=limit, offset=offset)
        photos = await photos_loads.all()
        photos = [photo.to_dict() for photo in photos]
        users = await load_users().all()
        users = [user.to_dict() for user in users]
        photos = {'photos': photos, 'users': users}
    else:
        photos_loads = load_photos(user=user, limit=limit, offset=offset)
        photos = await photos_loads.all()
        photos = [{'id': str(photo.id), 'path': photo.path} for photo in photos]
    return json(photos)


@doc.summary('Получение Количества фотографий')
@doc.security(True)
@doc.response(200, doc.Dictionary({'photo_count': doc.Integer()}))
@blueprint.get('/count')
@protected()
async def get_count(request: Request):  # pylint: disable=unused-argument
    count, *_ = await db \
        .select([func.count(Photo.id)]) \
        .gino.first()
    return json({'photo_count': count})


@doc.summary('Добавление новой оценки')
@doc.security(True)
@doc.consumes({'photo_id': doc.Integer()})
@doc.consumes({'rating': doc.Integer()})
@doc.response(200, doc.Dictionary({'status': doc.String('ok')}))
@blueprint.post('')
@protected()
@inject_user()
async def add_rating_photo(request: Request, user: User):
    photo_id = request.json.get('photo_id')
    rating = request.json.get('rating')
    raise_if_empty(photo_id, rating)
    raise_if_not_float(rating)
    await Assessment.create(
        photo_id=photo_id,
        user_id=user.id,
        rating=float(rating)
    )
    return json({'status': 'ok'})
