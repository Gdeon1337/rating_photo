import sys
import uuid
from base64 import b64encode
from datetime import datetime, timedelta
from decimal import Decimal
from enum import Enum
from typing import Any, Dict, Iterable, Tuple

from gino.crud import CRUDModel as _CRUDModel
from sqlalchemy.sql import expression as sql_expression
from sqlalchemy.sql.elements import BinaryExpression


if 'sanic' in sys.modules:
    from gino.ext.sanic import Gino as _Gino
else:
    from gino import Gino as _Gino


class CRUDModel(_CRUDModel):
    __hiden_keys__ = ()

    def to_dict(self) -> Dict:
        data = {}
        for key in list(self.__dict__.get('__values__', {}).keys()) + list(self.__dict__.keys()):
            if key.startswith('_') or key in getattr(self, '__hiden_keys__', []):
                continue
            value = getattr(self, key, None)
            if isinstance(value, uuid.UUID):
                value = str(value)
            elif isinstance(value, Decimal):
                value = float(value)
            elif isinstance(value, datetime):
                value = value.isoformat(' ')
            elif isinstance(value, timedelta):
                value = value.total_seconds()
            elif isinstance(value, Enum):
                value = value.value
            elif isinstance(value, bytes):
                value = b64encode(value).decode()
            elif isinstance(value, _CRUDModel):
                value = value.to_dict()
            data[key] = value
        return data

    def equal_tuple(self) -> Tuple[Any]:
        if not hasattr(self, '__equal_keys__'):
            return tuple()
        return tuple(getattr(self, equal_key, None) for equal_key in getattr(self, '__equal_keys__', []))

    def equal_hash(self) -> str:
        return str(uuid.uuid5(uuid.NAMESPACE_URL, ' '.join(tuple(map(str, self.equal_tuple())))))

    @classmethod
    def equal_in(cls, other: Iterable) -> BinaryExpression:
        equal_columns = cls.equal_tuple(cls)
        nullable_columns = [column.is_(None) for column in equal_columns if getattr(column, 'nullable', None)]
        return sql_expression.or_(sql_expression.tuple_(*equal_columns).in_(other), *nullable_columns)

    @classmethod
    def equal_query(cls, other: _CRUDModel) -> BinaryExpression:
        query = cls.query
        for column_name in getattr(cls, '__equal_keys__', []):
            cls_column = getattr(cls, column_name, None)
            other_column = getattr(other, column_name, None)
            if cls_column is not None and other_column is not None:
                query = query.where(cls_column == other_column)
        return query


class Gino(_Gino):
    model_base_classes = (CRUDModel,)


db = Gino()
