import copy

from ..server import Base, Column, String, Text, ForeignKey, relationship, Float, FLOAT, DECIMAL
from ..alignment.align import Align
from ..model import Bridge, Span
from ezdxf.math import Vec2, Matrix44, Vector


class std_Foundations(object):
    pass


class GeneralFoundation(Base):
    __tablename__ = "found_tbl"
    Name = Column("name", String(17), primary_key=True)
    _fSpan_name = Column('span_name', String(17),
                         ForeignKey("span_tbl.name", ondelete='CASCADE', onupdate='CASCADE'))
    RelatedSpan = relationship("Span", foreign_keys=[_fSpan_name], cascade='save-update,delete')
    TypeName = Column("type_name", String(10))

    def __init__(self, type_name: str, **kwargs):
        """
        通用基础类, 不直接实例化.

        Args:
            type_name: 类别名称.
            **kwargs:
        """
        self.TypeName = type_name
        pass


class Pile(Base):
    __tablename__ = "pile_tbl"
    Name = Column("name", String(17), primary_key=True)
    _fFund_name = Column('found_name', String(17),
                         ForeignKey("found_tbl.name", ondelete='CASCADE', onupdate='CASCADE'))
    RelatedFoundation = relationship("GeneralFoundation", foreign_keys=[_fFund_name], cascade='save-update,delete')
    X = Column('X', DECIMAL(20, 8), default=0.0)
    Y = Column('Y', DECIMAL(20, 8), default=0.0)
    Z = Column('Z', DECIMAL(20, 8), default=0.0)
    Length = Column('Length', DECIMAL(20, 8), default=0.0)
    Diameter = Column('Diameter', DECIMAL(20, 8), default=0.0)

    def __init__(self, xx: float, yy: float, zz: float, diameter: float, length: float, **kwargs):
        """
        通用桩基类.

        Args:
            xx: 桩顶 x
            yy: 桩顶 y
            zz: 桩顶 z
            diameter: 直径 (m)
            length: 桩长 (m)
            **kwargs:
        """
        self.X = xx
        self.Y = yy
        self.Z = zz
        self.Diameter = diameter
        self.Length = length
        pass

    def transform(self, mat: Matrix44):
        v0 = Vector(self.X, self.Y, self.Z)
        v1 = mat.transform(v0)
        self.X = v1.x
        self.Y = v1.y
        self.Z = v1.z


class RectPileCap(Base):
    __tablename__ = "RectPileCap_tbl"
    Name = Column("name", String(17), primary_key=True)
    _fFund_name = Column('found_name', String(17),
                         ForeignKey("found_tbl.name", ondelete='CASCADE', onupdate='CASCADE'))
    RelatedFoundation = relationship("GeneralFoundation", foreign_keys=[_fFund_name], cascade='save-update,delete')
    X = Column('X', DECIMAL(15, 3), default=0.0)
    Y = Column('Y', DECIMAL(15, 3), default=0.0)
    Z = Column('Z', DECIMAL(15, 3), default=0.0)
    AngOfNorth = Column('AngOfNorth', DECIMAL(15, 3), default=0.0)
    W = Column('W', DECIMAL(15, 3), default=0.0)
    L = Column('L', DECIMAL(15, 3), default=0.0)
    H = Column('H', DECIMAL(15, 3), default=0.0)

    def __init__(self, xx: float, yy: float, zz: float,
                 length: float, width: float, height: float,
                 **kwargs):
        """
        适用于一切矩形桩基承台，也适用于地系梁。

        Args:
            xx: 承台顶面型心 x
            yy: 承台顶面型心 y
            zz: 承台顶面型心 z
            length:
            width:
            height:
            **kwargs:
        """
        self.X = xx
        self.Y = yy
        self.Z = zz
        self.L = length
        self.W = width
        self.H = height

    def transform(self, mat: Matrix44):
        v0 = Vector(self.X, self.Y, self.Z)
        v1 = mat.transform(v0)
        self.X = v1.x
        self.Y = v1.y
        self.Z = v1.z


class RectPileFoundation(object):
    PileCapList = []
    PileList = []
    Found_Inst = None

    def __init__(self, type_name: str,
                 length: float, width: float, height: float,
                 cc_l: float, cc_w: float,
                 pile_num_l: int, pile_num_w: int,
                 pile_dia: float, pile_len: float, **kwargs):
        """
        矩形桩基，适用于一切矩形承台的桩基础，也适用于含地系梁的桩柱式基础。

        Args:
            type_name (str): 类别名称
            length (float): 基本尺寸L,顺桥向长度.
            width (float): 基本尺寸W,横桥向宽度,地系梁基础时为桩中距.
            height (float): 基本尺寸H,高度.
            cc_l (float): 顺桥向桩中距 (m)
            cc_w (float): 横桥向桩中距 (m)
            pile_num_l (int): 顺桥向桩基个数
            pile_num_w (int): 横桥向桩基个数
            pile_dia (float): 桩径 (m)

        """
        self.Found_Inst = GeneralFoundation(type_name)
        self.L = length
        self.W = width
        self.H = height
        self.PileDia = pile_dia
        self.Pile_CC_W = cc_w
        self.Pile_CC_L = cc_l

        cc0 = Vec2([(pile_num_w - 1) * cc_w * (-0.5), (pile_num_l - 1) * cc_l * (-0.5)])
        for ll in range(pile_num_l):
            for ww in range(pile_num_w):
                pt = cc0 + Vec2(ww * cc_w, ll * cc_l)
                pi = Pile(pt.x, pt.y, -self.H, pile_dia, pile_len)
                self.PileList.append(pi)
        self.PileCapList.append(RectPileCap(0, 0, 0, length, width, height))
        pass

    def transform(self, mat: Matrix44):
        """
        坐标变换
        Args:
            mat:

        Returns:

        """
        for pile in self.PileList:
            pile.transform(mat)
        for pc in self.PileCapList:
            pc.transform(mat)

    def copy(self):
        m1 = copy.deepcopy(self)
        m1.Found_Inst = copy.deepcopy(self.Found_Inst)
        m1.PileList = copy.deepcopy(self.PileList)
        m1.PileCapList = copy.deepcopy(self.PileCapList)
        for p in m1.PileList:
            p.RelatedFoundation = m1.Found_Inst
        for pc in m1.PileCapList:
            pc.RelatedFoundation = m1.Found_Inst
        return m1
