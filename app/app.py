from sanic import Blueprint, Sanic

from . import config


def create_app(config_object: object = config.Config) -> Sanic:
    app = Sanic()
    app.config.from_object(config_object)
    register_blueprints(app)
    register_extensions(app)
    return app


def register_extensions(app: Sanic):
    from . import extensions  # pylint: disable=import-outside-toplevel
    extensions.register_async_helpers(app)
    extensions.register_args_parser(app)
    extensions.register_ddtrace(app)
    extensions.register_db(app)
    extensions.register_redis(app)
    extensions.register_argon2(app)
    extensions.register_jwt(app)
    extensions.register_openapi(app)
    extensions.register_cors(app)


def register_blueprints(app: Sanic):
    from . import blueprints  # pylint: disable=import-outside-toplevel
    app.blueprint(Blueprint.group(
        blueprints.users.blueprint,
        blueprints.answers.blueprint,
        blueprints.exceptions.blueprint_exceptions,
        url_prefix=app.config.APP_URL_PREFIX
    ))
