import pytest

from tests import setup


@pytest.fixture
def engine():
    with setup.engine_factory() as _:
        yield _


@pytest.fixture
def database(engine):
    with setup.database_factory(engine) as _:
        yield _


@pytest.fixture
def session_factory(database, engine):
    with setup.session_factory(
        database, engine
    ) as _:
        yield _


@pytest.fixture
def session(session_factory):
    s = session_factory()
    yield s
    s.close()
