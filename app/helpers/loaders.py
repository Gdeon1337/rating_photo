from datetime import datetime
from typing import List, Optional, Union

from gino.api import GinoExecutor
from sqlalchemy.sql import Select, and_, func, or_

from database import User, db
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
