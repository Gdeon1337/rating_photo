import os
import socket
from typing import Dict, List, Tuple

import toml
from pyroute2 import IPDB
from sanic.log import LOGGING_CONFIG_DEFAULTS
from sanic_envconfig import EnvConfig


app_dir = os.path.abspath(os.path.dirname(__file__))
project_root = os.path.abspath(os.path.join(app_dir, os.pardir))
pyproject_info = toml.load(os.path.join(project_root, 'pyproject.toml'))
poetry_info = pyproject_info['tool']['poetry']

service_name = poetry_info["name"]
service_version = poetry_info['version']

with IPDB() as ipdb:
    default_gateway = ipdb.routes['default']['gateway']

default_ip = 'localhost'
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as dns_socket:
    try:
        dns_socket.connect(('8.8.8.8', 80))
        default_ip, _ = dns_socket.getsockname()
    except Exception:  # pylint: disable=broad-except
        pass


LOGGING_CONFIG_DEFAULTS['loggers'].update({
    'ddtrace': {'level': 'CRITICAL'}
})


class Config(EnvConfig):
    SERVER_IP: str = default_ip
    SERVER_PORT: int = 80
    DEFAULT_GATEWAY: str = default_gateway
    APP_URL_PREFIX: str = '/api'
    PROXIES_COUNT: int = 0  # If use NGINX set to 1

    PG_CONNECTION: str = None
    REDIS_CONNECTION: str = None

    GRACEFUL_SHUTDOWN_TIMEOUT: float = 5.0
    DB_POOL_MAX_SIZE: int = 64

    APP_DIR: str = app_dir
    PROJECT_ROOT: str = project_root

    PRODUCTION: bool = False
    DEBUG: bool = False
    ENVIRONMENT: str = 'production'
    IS_DOCKER: bool = False
    DDTARCE_HOSTNAME: str = 'localhost'

    SERVICE_NAME: str = service_name
    SERVICE_VERSION: str = service_version

    API_TITLE: str = service_name.title()
    API_VERSION: str = poetry_info['version']
    API_DESCRIPTION: str = poetry_info['description']
    API_SCHEMES: Tuple[str] = ('http', 'https')
    API_SECURITY: List[Dict] = [
        {
            'HeaderAccessToken': []
        }
    ]
    API_SECURITY_DEFINITIONS = {
        'HeaderAccessToken': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    }

    SANIC_JWT_SECRET: str = f'{service_name} JWT super-super secret'
    SANIC_JWT_STRICT_SLASHES: bool = True
    SANIC_JWT_PATH_TO_AUTHENTICATE: str = ''
    SANIC_JWT_BLUEPRINT_NAME: str = 'auth'
    SANIC_JWT_URL_PREFIX: str = f'{APP_URL_PREFIX}/{SANIC_JWT_BLUEPRINT_NAME}'
    SANIC_JWT_COOKIE_SET: bool = True
    SANIC_JWT_COOKIE_STRICT: bool = False
    SANIC_JWT_EXPIRATION_DELTA: int = 12 * 60 * 60
    SANIC_JWT_USER_ID: str = 'id'
    SANIC_JWT_REFRESH_TOKEN_ENABLED: bool = True

    CORS_AUTOMATIC_OPTIONS: bool = True
    CORS_SUPPORTS_CREDENTIALS: bool = True
    CORS_ORIGINS: Tuple[str] = ('.*',)
    CORS_SEND_WILDCARD: bool = False
