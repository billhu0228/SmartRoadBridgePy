from .base import *
from ..server import Base, Column, String, Text, ForeignKey, relationship, Float, DECIMAL


class PierBase(Base):
    __tablename__ = "sub_tbl"
    _fName = Column("Name", String(17), primary_key=True)
    _fSpa_name = Column('span_name', String(17), ForeignKey("span_tbl.name"))
    _fAli_name = Column('align_name', String(10), ForeignKey("ei_tbl.name"))
    _fBri_name = Column('bridge_name', String(10), ForeignKey("bridge_tbl.name"))
    span = relationship("Span", foreign_keys=[_fSpa_name], cascade='all')
    align = relationship("Align", foreign_keys=[_fAli_name], cascade='all')
    bridge = relationship("Bridge", foreign_keys=[_fBri_name], cascade='all')
    _fStation = Column('Station', DECIMAL(15, 3))
    _fAngle = Column('Angle', DECIMAL(15, 3))
    _fH0 = Column('H0', DECIMAL(15, 3))
    _fType = Column("Type", String(10))
    _fLeftWidth = Column('LeftWidth', DECIMAL(15, 3))
    _fRightWidth = Column('RightWidth', DECIMAL(15, 3))
    _fSpaceList = Column("SpaceList", String(100))
    _fPierAngleList = Column("PierAngleList", String(100))
    _fFundAngleList = Column("FundAngleList", String(100))
    _fH1List = Column("H1List", String(100))
    _fSlopeLeft = Column('SlopeLeft', DECIMAL(15, 3))
    _fSlopeRight = Column('SlopeRight', DECIMAL(15, 3))
    _fSlopeReal = Column('SlopeReal', DECIMAL(15, 3))


class OneColumnPier(PierBase):
    """
    独柱墩, 墩中心与设计线跨径线交点重合

    Keyword Args:
        class_name(str) : 类别.

    """

    def __init__(self, class_name: str):
        self._fType = class_name


if __name__ == "__main__":
    C1 = OneColumnPier(section="4*1.6")
    t = 1
