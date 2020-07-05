from uuid import uuid4

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from .db import db


class User(db.Model):
    __tablename__ = 'users'
    __hiden_keys__ = ('password',)

    id = db.Column(UUID(), primary_key=True, default=uuid4, server_default=func.uuid_generate_v4(), comment='ID пользователя')  # noqa

    login = db.Column(db.String(), nullable=False, comment='Логин пользователя')  # noqa
    password = db.Column(db.LargeBinary(), nullable=False, comment='Пароль пользователя')  # noqa
