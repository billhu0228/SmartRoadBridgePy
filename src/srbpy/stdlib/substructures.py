# -*- coding : utf-8-*-
import copy

from ..server import Base, Column, String, Text, ForeignKey, relationship, Float, FLOAT, DECIMAL, Integer
# from ..alignment.align import Align
# from ..model import Bridge, Span
from ezdxf.math import Vec2, Matrix44, Vec3


class std_Piers():
    pass


class std_Abutments():
    pass


class GeneralSub(Base):
    __tablename__ = "sub_tbl"
    Name = Column("name", String(17), primary_key=True)
    _fSpan_name = Column('span_name', String(17),
                         ForeignKey("span_tbl.name", ondelete='CASCADE', onupdate='CASCADE'))
    RelatedSpan = relationship("Span", foreign_keys=[_fSpan_name], cascade='save-update,delete')
    TypeName = Column("type_name", String(10))

    def __init__(self, type_name: str, **kwargs):
        """
        通用下部类, 不直接实例化.

        Args:
            type_name: 类别名称.
            **kwargs:
        """
        self.TypeName = type_name
        pass


class PierColumn(Base):
    __tablename__ = "column_tbl"
    Name = Column("name", String(20), primary_key=True)
    _fSub_name = Column('sub_name', String(17),
                        ForeignKey("sub_tbl.name", ondelete='CASCADE', onupdate='CASCADE'))
    RelatedSubstructure = relationship("GeneralSub", foreign_keys=[_fSub_name], cascade='save-update,delete')
    X = Column('X', DECIMAL(20, 8), default=0.0)
    Y = Column('Y', DECIMAL(20, 8), default=0.0)
    Z = Column('Z', DECIMAL(20, 8), default=0.0)
    AngOfNorth = Column('AngOfNorth', DECIMAL(15, 3), default=0.0)
    W = Column('W', DECIMAL(15, 3), default=0.0)
    L = Column('L', DECIMAL(15, 3), default=0.0)
    H = Column('H', DECIMAL(15, 3), default=0.0)
    Diameter = Column('Diameter', DECIMAL(20, 8), default=0.0)

    def __init__(self, xx: float, yy: float, zz: float,
                 length: float = 0.0, width: float = 0.0, height: float = 0.0,
                 diameter: float = 0.0, **kwargs):
        """
        矩形（圆形）墩柱类.

        Args:
            xx: 柱顶 x
            yy: 柱顶 y
            zz: 柱顶 z
            length:
            width:
            height:
            diameter: 直径 (m)
            **kwargs:
        """
        self.X = xx
        self.Y = yy
        self.Z = zz
        self.Diameter = diameter
        self.L = length
        self.W = width
        self.H = height
        pass

    def transform(self, mat: Matrix44):
        v0 = Vec3(self.X, self.Y, self.Z)
        v1 = mat.transform(v0)
        self.X = v1.x
        self.Y = v1.y
        self.Z = v1.z


class CapBeam(Base):
    __tablename__ = "capbeam_tbl"
    Name = Column("name", String(17), primary_key=True)
    _fSub_name = Column('sub_name', String(17),
                        ForeignKey("sub_tbl.name", ondelete='CASCADE', onupdate='CASCADE'))
    RelatedSubstructure = relationship("GeneralSub", foreign_keys=[_fSub_name], cascade='save-update,delete')
    X = Column('X', DECIMAL(20, 8), default=0.0)
    Y = Column('Y', DECIMAL(20, 8), default=0.0)
    Z = Column('Z', DECIMAL(20, 8), default=0.0)
    AngOfNorth = Column('AngOfNorth', DECIMAL(15, 3), default=0.0)
    WL = Column('WL', DECIMAL(15, 3), default=0.0)
    WR = Column('WR', DECIMAL(15, 3), default=0.0)
    L = Column('L', DECIMAL(15, 3), default=0.0)
    H = Column('H', DECIMAL(15, 3), default=0.0)
    HP = Column('HP', DECIMAL(15, 3), default=0.0)

    def __init__(self, xx: float, yy: float, zz: float,
                 length: float, width_left: float, width_right: float, height: float,
                 cross_slope: float, **kwargs):
        """
        适用于一切单平面盖梁（包括虚拟盖梁）。

        Args:
            xx: 盖梁中心控制点 x
            yy: 盖梁中心控制点 y
            zz: 盖梁中心控制点 z
            length: 顺桥向长度
            width_left: 横桥向左宽
            width_right: 横桥向右宽
            height: 高度，可为零
            cross_slope: 横坡
            **kwargs:
        """
        self.X = xx
        self.Y = yy
        self.Z = zz
        self.L = length
        self.WL = width_left
        self.WR = width_right
        self.H = height
        self.HP = cross_slope

    def transform(self, mat: Matrix44):
        v0 = Vec3(self.X, self.Y, self.Z)
        v1 = mat.transform(v0)
        self.X = v1.x
        self.Y = v1.y
        self.Z = v1.z


# ============================================================================================= #
# 以下为用户使用下部结构类型
# ============================================================================================= #

class OneColumnPier(object):
    Sub_Inst = None
    ColumnList = []
    CapBeam_Inst = None

    def __init__(self, type_name: str,
                 cb_length: float, cb_width_left: float, cb_width_right: float, cb_height: float, cb_hp: float,
                 col_length: float = 0.0, col_width: float = 0.0, col_diameter: float = 0.0, col_embed: float = 0.5,
                 **kwargs):
        """
        独柱墩实例

        Args:
            type_name: 类型名称
            cb_length: 盖梁顺桥向长度
            cb_width_left: 盖梁参考点左宽（投影）
            cb_width_right: 盖梁参考点右宽（投影）
            cb_height: 盖梁高度，0时为虚拟盖梁
            cb_hp: 盖梁横坡
            col_length: 柱式墩顺桥向尺寸，0时为圆柱墩
            col_width: 柱式墩横桥向尺寸，0时为圆柱墩
            col_diameter:  柱式墩直径，0时为矩形墩，不可与长宽同时为0
            col_embed: 如土深度，默认为0.5m
            **kwargs:
        """
        # 不同时取0.
        assert col_diameter + col_width + col_length != 0
        if col_length * col_width == 0:
            assert col_length + col_width == 0
            assert col_diameter != 0
        if col_diameter == 0:
            assert col_length * col_width != 0
        #
        self.Sub_Inst = GeneralSub(type_name)
        self.CapBeam_Inst = CapBeam(0, 0, 0, cb_length, cb_width_left, cb_width_right, cb_height, cb_hp)
        self.ColumnList.append(PierColumn(0, 0, -cb_height, col_length, col_width, 10.0, col_diameter))
        self.Pier_embed = col_embed
        pass

    def transform(self, mat: Matrix44):
        """
        坐标变换
        Args:
            mat:

        Returns:

        """
        for col in self.ColumnList:
            col.transform(mat)
        self.CapBeam_Inst.transform(mat)

    def copy(self):
        m1 = copy.deepcopy(self)
        m1.Sub_Inst = copy.deepcopy(self.Sub_Inst)
        m1.CapBeam_Inst = copy.deepcopy(self.CapBeam_Inst)
        m1.ColumnList = copy.deepcopy(self.ColumnList)
        for col in m1.ColumnList:
            col.RelatedSubstructure = m1.Sub_Inst
        m1.CapBeam_Inst.RelatedSubstructure = m1.Sub_Inst
        return m1
