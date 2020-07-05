import json
from distutils.util import strtobool
from typing import Iterable
from uuid import UUID

from sanic.exceptions import InvalidUsage


def raise_if_not_limit(*args, error: str = 'Not limit.'):
    for arg in args:
        if arg is None:
            raise InvalidUsage(error)


def raise_if_empty(*args, error: str = 'Missing data.'):
    for arg in args:
        if arg is None:
            raise InvalidUsage(error)


def raise_if_not_uuid(*args, error: str = 'Incorrect data.'):
    for arg in args:
        try:
            UUID(str(arg))
        except ValueError:
            raise InvalidUsage(error)


def raise_if_not_bool(*args, error: str = 'Incorrect data.'):
    for arg in args:
        try:
            strtobool(str(arg))
        except ValueError:
            raise InvalidUsage(error)


def raise_if_not_int(*args, error: str = 'Incorrect data.'):
    for arg in args:
        if not str(arg).isdigit():
            raise InvalidUsage(error)


def raise_if_not_enum_class(*args, enum_class, error: str = 'Incorrect data.'):
    for arg in args:
        try:
            enum_class(str(arg))
        except ValueError:
            raise InvalidUsage(error)


def raise_if_not_float(*args, error: str = 'Incorrect data.'):
    for arg in args:
        if not str(arg).replace('.', '').isdigit():
            raise InvalidUsage(error)


def raise_if_not_json(*args, error: str = 'Incorrect data.'):
    for arg in args:
        try:
            json.loads(str(arg))
        except (ValueError, json.JSONDecodeError):
            raise InvalidUsage(error)


def raise_if_not_mime_type(mime_types: Iterable[str], *args, error: str = 'Incorrect data.'):
    for arg in args:
        if hasattr(arg, 'type') and str(arg.type) not in mime_types:
            raise InvalidUsage(error)
