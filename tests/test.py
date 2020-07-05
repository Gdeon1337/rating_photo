import pytest

from app import create_app


@pytest.yield_fixture(scope='module', autouse=True)
def app():
    app_ = create_app()
    yield app_


@pytest.fixture(autouse=True)
def test_cli(loop, app, sanic_client):
    return loop.run_until_complete(sanic_client(app))
