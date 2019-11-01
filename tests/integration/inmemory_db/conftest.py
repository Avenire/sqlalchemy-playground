import pytest

from tests import setup


@pytest.fixture(scope='session')
def engine():
    with setup.engine_factory() as _:
        yield _


@pytest.fixture(scope='session')
def database(engine):
    with setup.database_factory(engine) as _:
        yield _


@pytest.fixture(scope='session')
def session_factory(database, engine):
    with setup.session_factory(database, engine) as _:
        yield _


@pytest.fixture
def session(session_factory):
    sess = session_factory()
    sess.commit = sess.flush
    yield sess
    sess.rollback()
    sess.close()
