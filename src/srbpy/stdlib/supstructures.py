from ..server import Base, Column, String, Text, ForeignKey, relationship, Float, FLOAT, DECIMAL
from ..server.orm import Base


class std_Beams(object):
    pass


# class CIPBox(Base):
#     __tablename__ = "cip_box_tbl"
#     _fName = Column("Name", String(17), primary_key=True)
#     _fAli_name = Column('align_name', String(10),
#                         ForeignKey("ei_tbl.name", ondelete='CASCADE', onupdate='CASCADE'))
#     _fBri_name = Column('bridge_name', String(10),
#                         ForeignKey("bridge_tbl.name", ondelete='CASCADE', onupdate='CASCADE'))
#     align = relationship("Align", foreign_keys=[_fAli_name], cascade='save-update,delete')
#     bridge = relationship("Bridge", foreign_keys=[_fBri_name], cascade='save-update,delete')
#
#     _fStation_Start = Column('Station', DECIMAL(15, 3))
#     _fStation_End = Column('Station', DECIMAL(15, 3))
#
#     _fSpan0 = Column('span_0', String(17),
#                      ForeignKey("span_tbl.name", ondelete='CASCADE', onupdate='CASCADE'), nullable=True)
#     _fSpan1 = Column('span_1', String(17),
#                      ForeignKey("span_tbl.name", ondelete='CASCADE', onupdate='CASCADE'), nullable=True)
#     _fSpan2 = Column('span_2', String(17),
#                      ForeignKey("span_tbl.name", ondelete='CASCADE', onupdate='CASCADE'), nullable=True)
#     _fSpan3 = Column('span_3', String(17),
#                      ForeignKey("span_tbl.name", ondelete='CASCADE', onupdate='CASCADE'), nullable=True)
#     _fSpan4 = Column('span_4', String(17),
#                      ForeignKey("span_tbl.name", ondelete='CASCADE', onupdate='CASCADE'), nullable=True)
#     _fSpan5 = Column('span_5', String(17),
#                      ForeignKey("span_tbl.name", ondelete='CASCADE', onupdate='CASCADE'), nullable=True)
#     span0 = relationship("Span", foreign_keys=[_fSpan0], cascade='save-update,delete')
#     span1 = relationship("Span", foreign_keys=[_fSpan1], cascade='save-update,delete')
#     span2 = relationship("Span", foreign_keys=[_fSpan2], cascade='save-update,delete')
#     span3 = relationship("Span", foreign_keys=[_fSpan3], cascade='save-update,delete')
#     span4 = relationship("Span", foreign_keys=[_fSpan4], cascade='save-update,delete')
#     span5 = relationship("Span", foreign_keys=[_fSpan5], cascade='save-update,delete')
#
#
#     pass
