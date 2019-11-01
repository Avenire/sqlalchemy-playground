import pytest

from tests import setup
from tests.setup import composer


@pytest.fixture(scope='session')
@composer(setup.engine_factory)
def engine(): pass


@pytest.fixture(scope='session')
@composer(setup.database_factory)
def database(engine): pass


@pytest.fixture(scope='session')
@composer(setup.session_factory)
def session_factory(database, engine): pass


@pytest.fixture
def session(session_factory):
    sess = session_factory()
    sess.commit = sess.flush
    yield sess
    sess.rollback()
    sess.close()
