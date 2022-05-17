# -*- coding : utf-8-*-
import copy

from ..server import Base, Column, String, Text, ForeignKey, relationship, Float, FLOAT, DECIMAL, Integer
from ezdxf.math import Vec2, Matrix44, Vec3


class std_Joint(object):
    pass


class std_Bearing(object):
    pass


class Bearing(Base):
    __tablename__ = "bearing_tbl"
    Name = Column("name", String(17), primary_key=True)
    _fSpan_name = Column('span_name', String(17),
                         ForeignKey("span_tbl.name", ondelete='CASCADE', onupdate='CASCADE'))
    RelatedSpan = relationship("Span", foreign_keys=[_fSpan_name], cascade='save-update,delete')
    TypeName = Column("type_name", String(10))
    TotalHeight = Column('TotalHeight', DECIMAL(20, 8), default=0)
    BearingHeight = Column('BearingHeight', DECIMAL(20, 8), default=0)
    UpperHeight = Column('UpperHeight', DECIMAL(20, 8), default=0)
    X = Column('X', DECIMAL(20, 8), default=0.0)
    Y = Column('Y', DECIMAL(20, 8), default=0.0)
    Z = Column('Z', DECIMAL(20, 8), default=0.0)
    AngOfNorth = Column('AngOfNorth', DECIMAL(20, 8), default=0.0)

    def __init__(self, type_name: str, total_height: float, br_height: float, upper_height: float, **kwargs):
        """
        通用支座

        Args:
            type_name: 支座类型
            total_height: 支座系统总高度
            br_height: 支座高度
            upper_height: 支座上部结构（垫板，楔形块）高度
            **kwargs:
        """

        self.TypeName = type_name
        self.TotalHeight = total_height
        self.BearingHeight = br_height
        self.UpperHeight = upper_height
        pass
