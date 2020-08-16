from typing import Optional
from sqlalchemy import or_, not_
from sanic import Blueprint
from sanic.request import Request
from sanic.response import json
from database import Photo, db, Assessment, User
from sqlalchemy.sql import func, exists
from app.helpers.swagger import models as swagger_models
from sanic_openapi import doc  # pylint: disable=wrong-import-order
from sanic_jwt.decorators import inject_user, protected
from app.helpers.validators import raise_if_empty, raise_if_not_int, raise_if_not_float

blueprint = Blueprint('admin', url_prefix='/admin', strict_slashes=True)


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
    subq = db.select([Assessment.photo_id]).where(Assessment.user_id == user.id).as_scalar()
    query = Photo.query.where(not_(Photo.id.in_(subq)))
    photos = limit_query(query, limit, offset)
    photos = await photos.gino.all()
    photos = [{'id': str(photo.id), 'path': photo.path} for photo in photos]
    return json(photos)