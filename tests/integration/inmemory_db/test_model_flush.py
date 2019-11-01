from src.model import ParentJsonStats, Child


def test_adds_parent(session):
    parent = ParentJsonStats()
    session.add(parent)
    session.commit()
    assert parent == session.query(ParentJsonStats).filter(
        ParentJsonStats.parent_id == parent.parent_id
    ).one()


def test_adds_child(session):
    child = Child(
        name='child', num_something='1', parent_id='1'
    )
    session.add(child)
    session.commit()
    assert child == session.query(Child).filter(
        Child.child_id == child.child_id
    ).one()
