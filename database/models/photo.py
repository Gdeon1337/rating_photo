from uuid import uuid4

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from .db import db


class Photo(db.Model):
    __tablename__ = 'photos'

    id = db.Column(UUID(), primary_key=True, default=uuid4, server_default=func.uuid_generate_v4(), comment='Id photo.')  # noqa
    path = db.Column(db.String(), nullable=False, comment='Путь до фотографии')  # noqa
