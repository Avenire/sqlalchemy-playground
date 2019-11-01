import os
import functools
import uuid
from contextlib import contextmanager

from sqlalchemy.orm import scoped_session, sessionmaker

from src.model import Base


@contextmanager
def engine_factory():
    from sqlalchemy import create_engine
    user, password, host = (
        os.environ.get('PG_USER'), os.environ.get('PG_PASS'),
        os.environ.get('PG_HOST')
    )
    connection_string = f'postgresql+psycopg2://{user}:{password}@{host}'
    yield lambda db, *args, **kwargs: create_engine(
        '{}/{}'.format(connection_string, db), *args, **kwargs
    )


@contextmanager
def database_factory(create_engine):
    admin_database = os.environ.get('PG_ADMIN_DB', 'postgres')
    admin_engine = create_engine(admin_database, pool_size=1,
        execution_options={'isolation_level': 'AUTOCOMMIT'}
    )
    test_database = f'test_db_{str(uuid.uuid4()).replace("-", "_")}'
    admin_engine.execute(f'DROP DATABASE IF EXISTS {test_database}')
    admin_engine.execute(f'CREATE DATABASE {test_database}')
    yield test_database
    admin_engine.execute(f'DROP DATABASE {test_database}')
    admin_engine.dispose()


@contextmanager
def session_factory(database, engine_factory):
    engine = engine_factory(
        database, convert_unicode=True, pool_size=1
    )
    session_factory = scoped_session(
        sessionmaker(
            autocommit=False,
            autoflush=True,
            bind=engine
        )
    )
    Base.metadata.create_all(engine)
    yield session_factory
    engine.dispose()


def composer(ctx_manager_func):
    def decorator(_):
        @functools.wraps(_)
        def reusable_body(**kwargs):
            fixtures = list(kwargs.values())
            with ctx_manager_func(*fixtures) as _:
                yield _
        return reusable_body
    return decorator
