from ..server import Base, Column, String, Text, ForeignKey, relationship, Float, FLOAT, DECIMAL
from ..alignment.align import Align
from ..model import Bridge, Span
from ezdxf.math import Vec2


class std_Foundations(object):
    pass


class RectPileFund(Base):
    __tablename__ = "RectPileFund_tbl"
    Name = Column("name", String(17), primary_key=True)
    _fAli_name = Column('align_name', String(10),
                        ForeignKey("ei_tbl.name", ondelete='CASCADE', onupdate='CASCADE'))
    _fBri_name = Column('bridge_name', String(10),
                        ForeignKey("bridge_tbl.name", ondelete='CASCADE', onupdate='CASCADE'))
    _fSpan_name = Column('span_name', String(17),
                         ForeignKey("span_tbl.name", ondelete='CASCADE', onupdate='CASCADE'))
    align = relationship("Align", foreign_keys=[_fAli_name], cascade='save-update,delete')
    bridge = relationship("Bridge", foreign_keys=[_fBri_name], cascade='save-update,delete')
    span = relationship("Span", foreign_keys=[_fSpan_name], cascade='save-update,delete')

    X = Column('X', DECIMAL(15, 3), default=0.0)
    Y = Column('Y', DECIMAL(15, 3), default=0.0)
    Z = Column('Z', DECIMAL(15, 3), default=0.0)
    AngOfNorth = Column('AngOfNorth', DECIMAL(15, 3), default=0.0)
    W = Column('W', DECIMAL(15, 3), default=0.0)
    L = Column('L', DECIMAL(15, 3), default=0.0)
    H = Column('H', DECIMAL(15, 3), default=0.0)

    def __init__(self, name: str, align: Align, bridge: Bridge, span: Span, **kwargs):
        """
        矩形桩基，适用于一切矩形承台的桩基础，也适用于含地系梁的桩柱式基础。

        Args:
            name (str): 实例名称
            align (Align): 关联路线
            bridge (Bridge): 关联桥梁
            span (Span): 关联桥跨
            Z0 (float): 基础埋深 (单位: m).
            ang_deg (float): 斜交角, 正交时为90, 逆时针为正, 默认值为90.
            dist (float): 斜距, 向右为正，向左为负.
            W (float): 基本尺寸W,横桥向宽度,地系梁基础时为桩中距.
            L (float): 基本尺寸L,顺桥向长度.
            H (float): 基本尺寸H,高度.

        """
        self.Name = name
        self.align = align
        self.bridge = bridge
        self.span = span
        self.Z = kwargs["Z0"]
        cc = Vec2(align.get_coordinate(span.station))
        dir = Vec2(align.get_direction(span.station))
        cdir = dir.rotate_deg(Vec2["ang_deg"])

        pass
