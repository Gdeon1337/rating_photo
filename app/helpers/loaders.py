from datetime import datetime
from typing import List, Optional, Union

from gino.api import GinoExecutor
from sqlalchemy.sql import Select, and_, func, or_, not_, tuple_

from database import User, db, Photo, Assessment
from database.models.db import CRUDModel

from . import validators


def limit_query(query: Select, limit: Optional[str] = None, offset: Optional[str] = None) -> Select:
    if limit:
        validators.raise_if_not_int(limit)
        query = query.limit(int(limit))
    if offset:
        validators.raise_if_not_int(offset)
        query = query.offset(int(offset))
    return query


def admin_load_photos(limit: Optional[str] = None, offset: Optional[str] = None):
    alias_ass = Assessment.alias('ass')
    subq = db.select([Assessment]).where(Assessment.photo_id == alias_ass.photo_id).as_scalar()
    query = db.select((Photo, subq)).select_from(Photo.outerjoin(alias_ass))
    query = limit_query(query, limit, offset)

    return query.gino.load(Photo.load(assessments=subq))


def load_users():
    return User.query.where(User.login != 'admin').gino


def load_photos(user: User, limit: Optional[str] = None, offset: Optional[str] = None):
    alias_ass = Assessment.alias('ass')
    subq = db.select([Assessment.user_id]).where(Assessment.id == alias_ass.id).as_scalar()
    query = db.select([Photo]).select_from(Photo.outerjoin(alias_ass, or_(
        and_(alias_ass.user_id == user.id, alias_ass.photo_id == Photo.id), alias_ass.photo_id == None))). \
        where(not_(tuple_(user.id).in_(subq)))
    photos = limit_query(query, limit, offset)

    return photos.gino

