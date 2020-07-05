from uuid import uuid4

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from .db import db


class Assessment(db.Model):
    __tablename__ = 'assessments'

    id = db.Column(UUID(), primary_key=True, default=uuid4, server_default=func.uuid_generate_v4(), comment='ID оценки')
    rating = db.Column(db.Float(), nullable=True, comment='Рейтинг фотографии.')
    photo_id = db.Column(UUID(), db.ForeignKey('photos.id', ondelete='CASCADE'), nullable=True, index=True, comment='ID фотографии.')
    user_id = db.Column(UUID(), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=True, index=True, comment='ID пользователя.')
