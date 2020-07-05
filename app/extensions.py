import asyncio
from typing import Any, Dict, List, Optional

import aioredis
from ddtrace import tracer
from ddtrace.contrib.asyncio import context_provider
from ddtrace.contrib.logging import patch as ddtrace_logging_patch
from sanic import Sanic
from sanic.request import Request, RequestParameters
from sanic_cors import CORS
from sanic_openapi import swagger_blueprint  # pylint: disable=wrong-import-order

from database import db

from . import jwt
from .helpers import password_hasher, trace


def register_async_helpers(app: Sanic):
    app.run_in_executor = trace.run_in_executor
    app.gather_in_executor = trace.gather_in_executor
    app.gather = trace.gather
    app.create_task = trace.create_task


def register_args_parser(_):
    def get_separated(self, name: str, default: Optional[Any] = None, separator: str = ',') -> List[str]:
        value = self.get(name)
        if value:
            return value.split(separator)
        return default or []

    RequestParameters.get_separated = get_separated


def register_ddtrace(app: Sanic):
    ddtrace_logging_patch()
    if app.config.IS_DOCKER:
        app.config.DDTARCE_HOSTNAME = app.config.DEFAULT_GATEWAY
    tracer.configure(hostname=app.config.DDTARCE_HOSTNAME, context_provider=context_provider)
    app.register_middleware(trace.ddtarce_on_request, 'request')
    app.register_middleware(trace.ddtarce_on_response, 'response')


def register_openapi(app: Sanic):
    app.blueprint(swagger_blueprint)


def register_db(app: Sanic):
    app.config.DB_DSN = app.config.PG_CONNECTION
    app.config.DB_ECHO = app.config.DEBUG
    db.init_app(app)
    app.db = db


def register_redis(app: Sanic):
    async def create_redis_connection(app: Sanic, loop: asyncio.AbstractEventLoop):
        app.redis = await aioredis.create_redis(app.config.REDIS_CONNECTION, loop=loop)

    async def close_redis_connection(app: Sanic, _):
        if hasattr(app, 'redis'):
            app.redis.close()
            await app.redis.wait_closed()

    app.register_listener(create_redis_connection, 'before_server_start')
    app.register_listener(close_redis_connection, 'before_server_stop')


def register_cors(app: Sanic):
    app.cors = CORS(app)


def register_argon2(app: Sanic):
    app.argon2 = password_hasher.AsyncPasswordHasher()


def register_jwt(app: Sanic):
    app.jwt = jwt.JWT(
        app,
        authenticate=jwt.authenticate,
        retrieve_user=jwt.retrieve_user,
        store_refresh_token=jwt.store_refresh_token,
        retrieve_refresh_token=jwt.retrieve_refresh_token,
        class_views=[('/logout', jwt.Logout)],
    )
    jwt.swagger(app)


# def register_rabbitmq(app: Sanic):
#     async def create_rabbitmq_connection(app: Sanic, loop: asyncio.AbstractEventLoop):
#         app.rabbitmq_connection = await aio_pika.connect_robust(app.config.RABBITMQ_AMQP, loop=loop)
#         app.rabbitmq_channel = await app.rabbitmq_connection.channel()

#     async def close_rabbitmq_connection(app: Sanic, _):
#         if hasattr(app, 'rpc'):
#             await app.rpc.close()
#         if hasattr(app, 'rabbitmq_channel'):
#             await app.rabbitmq_channel.close()
#         if hasattr(app, 'rabbitmq_connection'):
#             await app.rabbitmq_connection.close()

#     app.register_listener(create_rabbitmq_connection, 'before_server_start')
#     app.register_listener(close_rabbitmq_connection, 'before_server_stop')
