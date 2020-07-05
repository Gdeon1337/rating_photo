from sanic_openapi import doc  # pylint: disable=wrong-import-order

import database


class User:
    id = doc.String(database.User.id.comment)
    login = doc.String(database.User.login.comment)
    password = doc.String(database.User.password.comment)


class Assessment:
    id = doc.String(database.Assessment.id.comment)
    rating = doc.String(database.Assessment.rating.comment)
    photo_id = doc.String(database.Assessment.photo_id.comment)
    user_id = doc.String(database.Assessment.user_id.comment)


class Photo:
    id = doc.String(database.Photo.id.comment)
    path = doc.String(database.Photo.path.comment)
