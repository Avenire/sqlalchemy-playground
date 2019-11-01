import pytest

from tests import setup
from tests.setup import composer


@pytest.fixture
@composer(setup.engine_factory)
def engine(): pass


@pytest.fixture
@composer(setup.database_factory)
def database(engine): pass


@pytest.fixture
@composer(setup.session_factory)
def session_factory(database, engine): pass


@pytest.fixture
def session(session_factory):
    s = session_factory()
    yield s
    s.close()
