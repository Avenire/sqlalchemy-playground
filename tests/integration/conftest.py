import os

import pytest

from tests.setup import engine_factory


@pytest.fixture(scope='session', autouse=True)
def cleanup_dangling_test_databases():
    admin_database = os.environ.get('PG_ADMIN_DB', 'postgres')
    with engine_factory() as ef:
        admin_engine = ef(
            admin_database, pool_size=1,
            execution_options={'isolation_level': 'AUTOCOMMIT'}
        )
        q = admin_engine.execute('SELECT datname FROM pg_database;')
        databases = [
            db_name for db_name in (row[0] for row in q.fetchall())
            if db_name.startswith('test_db')
        ]

        for db in databases:
            admin_engine.execute(f'DROP DATABASE {db}')

        admin_engine.dispose()
    yield
