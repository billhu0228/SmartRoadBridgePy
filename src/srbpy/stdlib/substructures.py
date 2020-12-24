import copy

from ..server import Base, Column, String, Text, ForeignKey, relationship, Float, FLOAT, DECIMAL
from ..alignment.align import Align
from ..model import Bridge, Span
from ezdxf.math import Vec2, Matrix44, Vector


class std_Piers():
    pass


class std_Abutments():
    pass


class SwapItem(Base):
    __tablename__ = "swap_tbl"
    Name = Column("name", String(17), primary_key=True)
    _fAli_name = Column('align_name', String(10), ForeignKey("ei_tbl.name", ondelete='CASCADE', onupdate='CASCADE'))
    _fBri_name = Column('bridge_name', String(10),
                        ForeignKey("bridge_tbl.name", ondelete='CASCADE', onupdate='CASCADE'))
    RelatedAlign = relationship("Align", foreign_keys=[_fAli_name], cascade='save-update,delete')
    RelatedBridge = relationship("Bridge", foreign_keys=[_fBri_name], cascade='save-update,delete')

    W = Column('W', DECIMAL(20, 8), default=0.0)
    H = Column('H', DECIMAL(20, 8), default=0.0)
    Z = Column('Z', DECIMAL(20, 8), default=0.0)
    Length = Column('Length', DECIMAL(20, 8), default=0.0)
    Diameter = Column('Diameter', DECIMAL(20, 8), default=0.0)
    pass
