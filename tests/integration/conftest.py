import pytest

from tests.setup import engine_factory


@pytest.fixture(scope='session', autouse=True)
def cleanup_db():
    admin_database = 'postgres'
    with engine_factory() as ef:
        admin_engine = ef(
            admin_database, pool_size=1,
            execution_options={'isolation_level': 'AUTOCOMMIT'}
        )
        q = admin_engine.execute(
            """
            SELECT
               datname
            FROM
               pg_database;
            """
        )
        available_tables = [x for x in (x[0] for x in q.fetchall()) if
                            x.startswith('test_db')]

        for db in available_tables:
            admin_engine.execute(f'DROP DATABASE IF EXISTS {db}')

        admin_engine.dispose()
    yield
