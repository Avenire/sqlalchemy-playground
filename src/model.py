from sqlalchemy import Column, String, Integer, select, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import column_property

Base = declarative_base()


def uuid():
    import uuid
    return str(uuid.uuid4())


class Child(Base):
    __tablename__ = 'child'
    name = Column(String(length=255), nullable=False)
    num_something = Column(Integer())
    child_id = Column(
        String(length=255), primary_key=True, default=uuid
    )
    # Intentionally not using foreign keys because of (bad) reasons.
    parent_id = Column(String(length=255), nullable=False)


class ParentBase(Base):
    __tablename__ = 'parent'
    parent_id = Column(String(length=255), primary_key=True, default=uuid)


class ParentJsonStats(ParentBase):

    _stats_selectable = (
        select([
            func.jsonb_build_object(
                'parent_id', Child.parent_id,
                'total_something', func.sum(Child.num_something),
                'num_children', func.count(Child.child_id)
            )
        ]).where(
            Child.parent_id == ParentBase.parent_id
        ).group_by(
            Child.parent_id
        )
    )
    _children_stats = column_property(
        _stats_selectable
    )

    @hybrid_property
    def total_something(self):
        return self._children_stats['total_something']

    @hybrid_property
    def num_children(self):
        return self._children_stats['num_children']


class ParentSeparateColumnPropsStats(ParentBase):
    total_something = column_property(
        select([
            func.sum(Child.num_something)
        ]).where(
            ParentBase.parent_id == Child.parent_id
        ).group_by(Child.parent_id)
    )
    num_children = column_property(
        select([
            func.count(Child.child_id)
        ]).where(
            ParentBase.parent_id == Child.parent_id
        ).group_by(Child.parent_id)
    )
