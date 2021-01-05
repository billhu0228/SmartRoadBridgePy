import copy

from ..server import Base, Column, String, Text, ForeignKey, relationship, Float, FLOAT, DECIMAL, Integer
from ezdxf.math import Vec2, Matrix44, Vector


class std_Joint(object):
    pass


class std_Bearing(object):
    pass


class GeneralBearing(Base):
    __tablename__ = "bearing_tbl"
    Name = Column("name", String(17), primary_key=True)
    _fSpan_name = Column('span_name', String(17),
                         ForeignKey("span_tbl.name", ondelete='CASCADE', onupdate='CASCADE'))
    RelatedSpan = relationship("Span", foreign_keys=[_fSpan_name], cascade='save-update,delete')
    TypeName = Column("type_name", String(10))

    def __init__(self, type_name: str, **kwargs):
        """
        支座系统类.

        Args:
            type_name: 类别名称.
            **kwargs:
        """
        self.TypeName = type_name
        pass
