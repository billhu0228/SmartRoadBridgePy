# -*- coding : utf-8-*-
import copy

from ..server import Base, Column, String, Text, ForeignKey, relationship, Float, FLOAT, DECIMAL, Integer
from ..server.orm import Base


class std_Beams(object):
    pass


class CIPBoxPoints(Base):
    __tablename__ = "cipboxpts_tbl"
    Name = Column("name", String(25), primary_key=True)
    _fBox_name = Column('box_name', String(17), ForeignKey("cipbox_tbl.name", ondelete='CASCADE', onupdate='CASCADE'))
    RelatedCIPBox = relationship("CIPBox", foreign_keys=[_fBox_name], cascade='save-update,delete')
    X = Column('X', DECIMAL(20, 8), default=0.0)
    Y = Column('Y', DECIMAL(20, 8), default=0.0)
    Z = Column('Z', DECIMAL(20, 8), default=0.0)

    def __init__(self, idx: int, x0: float, y0: float, z0: float):
        self.idx = idx
        self.X = x0
        self.Y = y0
        self.Z = z0
        pass

    def SetRelatedCIPBox(self, cipbox_inst):
        self.RelatedCIPBox = cipbox_inst
        self.Name = cipbox_inst.Name + str(self.idx).zfill(5)


class CIPBox(Base):
    __tablename__ = "cipbox_tbl"
    Name = Column("name", String(17), primary_key=True)
    _fAli_name = Column('align_name', String(10), ForeignKey("ei_tbl.name", ondelete='CASCADE', onupdate='CASCADE'))
    _fBri_name = Column('bridge_name', String(10),
                        ForeignKey("bridge_tbl.name", ondelete='CASCADE', onupdate='CASCADE'))
    RelatedAlign = relationship("Align", foreign_keys=[_fAli_name], cascade='save-update,delete')
    RelatedBridge = relationship("Bridge", foreign_keys=[_fBri_name], cascade='save-update,delete')

    _fSpan0 = Column('span0', String(17), ForeignKey("span_tbl.name", ondelete='CASCADE', onupdate='CASCADE'))
    _fSpan1 = Column('span1', String(17), ForeignKey("span_tbl.name", ondelete='CASCADE', onupdate='CASCADE'))
    _fSpan2 = Column('span2', String(17), ForeignKey("span_tbl.name", ondelete='CASCADE', onupdate='CASCADE'))
    _fSpan3 = Column('span3', String(17), ForeignKey("span_tbl.name", ondelete='CASCADE', onupdate='CASCADE'))
    _fSpan4 = Column('span4', String(17), ForeignKey("span_tbl.name", ondelete='CASCADE', onupdate='CASCADE'))
    _fSpan5 = Column('span5', String(17), ForeignKey("span_tbl.name", ondelete='CASCADE', onupdate='CASCADE'))
    _fSpan6 = Column('span6', String(17), ForeignKey("span_tbl.name", ondelete='CASCADE', onupdate='CASCADE'))
    _fSpan7 = Column('span7', String(17), ForeignKey("span_tbl.name", ondelete='CASCADE', onupdate='CASCADE'))
    RelatedSpan0 = relationship("Span", foreign_keys=[_fSpan0], cascade='save-update,delete')
    RelatedSpan1 = relationship("Span", foreign_keys=[_fSpan1], cascade='save-update,delete')
    RelatedSpan2 = relationship("Span", foreign_keys=[_fSpan2], cascade='save-update,delete')
    RelatedSpan3 = relationship("Span", foreign_keys=[_fSpan3], cascade='save-update,delete')
    RelatedSpan4 = relationship("Span", foreign_keys=[_fSpan4], cascade='save-update,delete')
    RelatedSpan5 = relationship("Span", foreign_keys=[_fSpan5], cascade='save-update,delete')
    RelatedSpan6 = relationship("Span", foreign_keys=[_fSpan6], cascade='save-update,delete')
    RelatedSpan7 = relationship("Span", foreign_keys=[_fSpan7], cascade='save-update,delete')
    W = Column('W', DECIMAL(20, 8), default=0.0)
    H = Column('H', DECIMAL(20, 8), default=0.0)
    start_pk = Column('StartPK', DECIMAL(20, 8), default=0.0)
    end_pk = Column('EndPK', DECIMAL(20, 8), default=0.0)
    LevelBottom = Column('LevelBottom', Integer, default=1)
    KeyPointsList = []

    def __init__(self, type_name: str,
                 width: float, height: float, level_bottom: bool):
        self.type_name = type_name
        self.W = width
        self.H = height
        self.LevelBottom = level_bottom
        pass

    def copy(self):
        m1 = copy.deepcopy(self)
        m1.KeyPointsList = []
        return m1

    def span_list(self):
        return [self._fSpan0, self._fSpan1, self._fSpan2, self._fSpan3, self._fSpan4, self._fSpan5, self._fSpan6,
                self._fSpan7, ]
