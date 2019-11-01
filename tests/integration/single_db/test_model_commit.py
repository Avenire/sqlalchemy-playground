import pytest

from src.model import (
    Child, ParentJsonStats, ParentBase, ParentSeparateColumnPropsStats
)


@pytest.fixture
def setup_data(session):
    num_children = 5
    num_parents = 10
    for id_ in map(str, range(num_parents)):
        parent = ParentBase(parent_id=id_)
        children = [
            Child(
                name=f'Child {id_}/{child_id}', num_something=1,
                parent_id=id_
            )
            for child_id in map(str, range(num_children))
        ]
        session.add_all([*children, parent])
    session.commit()


@pytest.mark.parametrize('parent_cls', [
    ParentJsonStats, ParentSeparateColumnPropsStats
])
def test_large_data(parent_cls, setup_data, session):
    parent_id = 'test_large_data'
    parent = parent_cls(parent_id=parent_id)
    expected_stats = 5
    children = [
        Child(
            name=f'Test `large` data {_}', num_something=1, parent_id=parent_id
        )
        for _ in map(str, range(expected_stats))
    ]
    session.add_all([*children, parent])

    parent = session.query(parent_cls).filter(
        parent_cls.parent_id == parent.parent_id
    ).one()
    assert parent.total_something == parent.num_children == expected_stats
