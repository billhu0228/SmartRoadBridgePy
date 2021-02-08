# -*- coding : utf-8-*-
import copy
import json
import os
import zipfile
import numpy as np
import sqlalchemy
from decimal import ROUND_HALF_UP, Decimal
from PyAngle import Angle
from numpy import loadtxt, pi
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from xml.dom.minidom import Document
from ..alignment.align import Align
from ..server import Base, Column, String, Text, ForeignKey, relationship, Float, FLOAT, DECIMAL
from ezdxf.math import Vec2, Matrix44, Vector
from ..stdlib.supstructures import CIPBoxPoints


class Bridge(Base):
    __tablename__ = "bridge_tbl"
    name = Column('name', String(10), primary_key=True)
    _f_ali_name = Column('align_name', String(10), ForeignKey("ei_tbl.name", ondelete='CASCADE', onupdate='CASCADE'))
    _f_title_name = Column('title_name', String(120), nullable=True)
    RelatedAlign = relationship("Align", foreign_keys=[_f_ali_name], cascade='save-update,delete')

    def __init__(self, name: str, al: Align):
        self.name = name
        self.RelatedAlign = al
        self.spanlist = []
        self.ciplist = []

    def set_title(self, title: str):
        self._f_title_name = title

    def serialize(self):
        return json.dumps({"name": self.name})

    def assign_sup(self, inst_name: str, inst: Base, spans: list, st_pk: float, end_pk: float, steps=0.1):
        """
        指定上部结构.

        Args:
            inst_name:
            inst:
            spans:
            st_pk:
            end_pk:
            steps: 现浇梁线段步长

        Returns:

        """
        sup_inst = inst.copy()
        sup_inst.Name = inst_name
        sup_inst.start_pk = st_pk
        sup_inst.end_pk = end_pk
        sup_inst.RelatedAlign = self.RelatedAlign
        sup_inst.RelatedBridge = self
        for ii, sp in enumerate(spans):
            setattr(sup_inst, "RelatedSpan%i" % ii, sp)
        # 补充KP
        npts = int((end_pk - st_pk) / steps) + 1
        sideL = ((end_pk - st_pk) - (npts - 3) * steps) * 0.5
        for i in range(npts):
            if i == 0:
                dx = st_pk
            elif i == npts - 1:
                dx = end_pk
            else:
                dx = st_pk + sideL + (i - 1) * steps
            x0, y0 = sup_inst.RelatedAlign.get_coordinate(dx)
            z0 = sup_inst.RelatedAlign.get_elevation(dx)
            KP = CIPBoxPoints(i, float(x0), float(y0), float(z0))
            KP.SetRelatedCIPBox(sup_inst)
            sup_inst.KeyPointsList.append(KP)
        #
        self.ciplist.append(sup_inst)
        pass


class Span(Base):
    # 增加ORM映射 -- Bill 2020/11/18
    __tablename__ = "span_tbl"
    name = Column("name", String(17), primary_key=True)
    _fAli_name = Column('align_name', String(10), ForeignKey("ei_tbl.name", ondelete='CASCADE', onupdate='CASCADE'))
    _fBri_name = Column('bridge_name', String(10),
                        ForeignKey("bridge_tbl.name", ondelete='CASCADE', onupdate='CASCADE'))
    align = relationship("Align", foreign_keys=[_fAli_name], cascade='save-update,delete')
    bridge = relationship("Bridge", foreign_keys=[_fBri_name], cascade='save-update,delete')

    _fStation = Column('Station', DECIMAL(15, 3))
    _fAngle = Column('Angle', DECIMAL(15, 3))
    _f_deck_wl = Column('deck_wl', DECIMAL(15, 3), nullable=True)
    _f_deck_wr = Column('deck_wr', DECIMAL(15, 3), nullable=True)
    _f_back_wl = Column('back_wl', DECIMAL(15, 3), nullable=True)
    _f_back_wr = Column('back_wr', DECIMAL(15, 3), nullable=True)
    _f_front_wl = Column('front_wl', DECIMAL(15, 3), nullable=True)
    _f_front_wr = Column('front_wr', DECIMAL(15, 3), nullable=True)
    _fBeam_type = Column('BeamType', String(1), nullable=True)
    _fPier_type = Column('PierType', String(1), nullable=True)
    _fDeck_type = Column('DeckType', String(2), nullable=True, default="CT")
    _fCut_to = Column("cut_to", String(17), nullable=True)
    _fCut_by = Column("cut_by", String(17), nullable=True)
    _fHPL = Column("HPL", DECIMAL(15, 3), nullable=True)
    _fHPR = Column("HPR", DECIMAL(15, 3), nullable=True)

    # 增加ORM映射 -- Bill 2020/11/18

    def __init__(self, align: Align, bridge: Bridge, station: float, ang_deg: float = 90):
        """
        跨径线对象

        Args:
            align (Align): 跨径线对应路线
            bridge (Bridge): 跨径线对应桥梁
            station (float): 跨径线桩号
            ang_deg (float): 斜交角, 正交时为90, 逆时针为正, 默认值为90.

        """
        self.align = align
        self.bridge = bridge
        self.station = station
        self.angle = Angle.from_degrees(ang_deg).to_rad()
        self.elevation = align.get_elevation(station)
        self.ground_elevation = align.get_ground_elevation(station, 0)
        self.width_left, self.width_right = align.get_width(station, self.angle)
        self.hp_left, self.hp_right = align.get_cross_slope(station, self.angle)

        self.pier = None
        self.foundation = None
        self.mj = None
        self.bearings = []
        # 增加ORM映射 -- Bill 2020/11/18
        result = ("%.3f" % (float(Decimal(station).quantize(Decimal('0.000'), rounding=ROUND_HALF_UP)))).zfill(9)
        self.name = align.name + "+" + result
        self._fStation = station
        self._fAngle = ang_deg
        self._fHPL = self.hp_left
        self._fHPR = self.hp_right
        self._f_deck_wl = self.width_left
        self._f_deck_wr = self.width_right
        # 增加ORM映射 -- Bill 2020/11/18
        self.pier = None  # 增加结构指定

    def __str__(self):
        return self.name

    def __eq__(self, other):
        if isinstance(other, Span):
            if str(self) == str(other):
                return True
        else:
            return False

    def __lt__(self, other):
        if isinstance(other, Span):
            return self.station < other.station
        else:
            raise Exception("无法与非Span类进行比较.")

    def __add__(self, dist: float):
        return Span(self.align, self.bridge, self.station + dist, self.angle)

    def __sub__(self, other) -> float:
        if isinstance(other, Span):
            if other.align == self.align:
                return self.station - other.station
            else:
                print("警告：桩号不在同一条设计线")
                return self.station - other.station
        raise Exception("无法与其他类型相减.")

    def serialize(self):
        dict = {
            "align": self.align.name,
            "bridge": self.bridge.name,
            "station": self.station,
            "angle": self.angle,
            "elevation": self.elevation,
            "ground_elevation": self.ground_elevation,
            "width_left": self.width_left,
            "width_right": self.width_right,
            "hp_left": self.hp_left,
            "hp_right": self.hp_right,
        }
        return json.dumps(dict)

    def assign_substructure(self, inst_name: str, sub_inst: Base):
        """
        向S附加下部结构
        Args:
            inst_name: 主键
            sub_inst: 实例

        Returns:

        """
        self.pier = sub_inst.copy()
        self.pier.Sub_Inst.Name = inst_name
        self.pier.Sub_Inst.RelatedSpan = self
        for ii, col in enumerate(self.pier.ColumnList):
            col.Name = inst_name + "/COL%s" % str(ii + 1).zfill(2)
        self.pier.CapBeam_Inst.Name = inst_name + "/CB01"
        xyz = self.align.get_coordinate(self.station)
        xyz.append(self.align.get_ground_elevation(self.station, 0))
        span_cc = Vector(xyz)
        uux = Vector(self.align.get_direction(self.station))
        uuy = uux.rotate_deg(90.0)
        uuz = Vector(0, 0, 1)
        trans_matrix = Matrix44.ucs(uux, uuy, uuz, span_cc)
        self.pier.transform(trans_matrix)
        pass

    def assign_found2(self, inst_name: str, fund_inst: Base):
        self.foundation = fund_inst.copy()
        self.foundation.Found_Inst.Name = inst_name
        self.foundation.Found_Inst.RelatedSpan = self
        for ii, pile in enumerate(self.foundation.PileList):
            pile.Name = inst_name + "/PI%s" % str(ii + 1).zfill(2)
        for ii, pc in enumerate(self.foundation.PileCapList):
            pc.Name = inst_name + "/PC%s" % str(ii + 1).zfill(2)
        xyz = self.align.get_coordinate(self.station)
        xyz.append(self.align.get_ground_elevation(self.station, 0))
        span_cc = Vector(xyz)
        uux = Vector(self.align.get_direction(self.station))
        uuy = uux.rotate_deg(90.0)
        uuz = Vector(0, 0, 1)
        trans_matrix = Matrix44.ucs(uux, uuy, uuz, span_cc)
        self.foundation.transform(trans_matrix)
        pass

    def assign_found(self, inst_name: str, fund_inst: Base,
                     off_l: float = 0, off_w: float = 0, off_h: float = 0,
                     angle_deg: float = 0):
        """
        指定属于本处分跨线的基础结构实例.

        Args:
            inst_name: 基础编号.
            fund_inst: 基础实例.
            off_h: 竖向偏心, 默认值为 0 表示地面线下0.5m.
            off_w: 横桥向偏心, 默认值为 0.
            off_l: 顺桥向偏心, 默认值为 0.
            angle_deg :基础相对于span平面的偏角, 默认值为 0, 逆时针为正.
        Returns:

        """
        self.foundation = copy.deepcopy(fund_inst)
        self.foundation.Name = inst_name
        self.foundation.align = self.align
        self.foundation.bridge = self.bridge
        self.foundation.RelatedSpan = self
        cc = Vec2(self.align.get_coordinate(self.station))
        l_unit = Vec2(self.align.get_direction(self.station))
        w_unit = l_unit.rotate_deg(90.0)
        delta = off_l * l_unit + off_w * w_unit
        new_cc = cc + delta
        z0 = self.align.get_ground_elevation(self.station, 0) - 0.5 + off_h
        x0 = new_cc.x
        y0 = new_cc.y
        ref_v = Vec2(self.align.get_direction(self.station))
        ref_v = ref_v.rotate_deg(Angle.from_rad(self.angle).to_degrees() + angle_deg - 90.0)
        ang2north = ref_v.angle_between(Vec2([0, 1]))
        self.foundation.AngOfNorth = ang2north  # 弧度
        self.foundation.X = x0
        self.foundation.Y = y0
        self.foundation.Z = z0

        pass

    def assign_bearing(self, inst_name: str, br_inst: Base, offset=None):
        """

        Args:
            inst_name:
            br_inst:
            offset:

        Returns:

        """

        if offset is None:
            offset = [0, 0]
        br_cp = br_inst.copy()

        br_cp.Name = inst_name
        br_cp.RelatedSpan = self
        bk_supper = None  # 后排上部
        ft_supper = None  # 前排上部
        supper = None
        for cip in self.bridge.ciplist:
            for ii, sp in enumerate(cip.span_list()):
                if sp.name == self.name:
                    if ii == 0:
                        ft_supper = cip
                    elif ii == len(cip.span_list()) - 1:
                        bk_supper = cip
                    else:
                        supper = cip

        xyz = self.align.get_coordinate(self.station)

        xyz.append()
        span_cc = Vector(xyz)

    def make_happy(self):
        pass
    # def assign_pier(self, name_inst: str, pier_inst: PierBase):
    #     """
    #     指定属于本处分跨线的桥墩结构实例.
    #
    #     Args:
    #         name: 桥墩编号.
    #         pier_inst: 桥墩实例.
    #
    #     Returns:
    #
    #     """
    #     self.pier = copy.deepcopy(pier_inst)
    #     self.pier._fName = name_inst
    #     self.pier.align = self.align
    #     self.pier.bridge = self.bridge
    #     self.pier.span = self
    #     self.pier._fStation = self._fStation
    #     self.pier._fAngle = self._fAngle
    #     self.pier._fSlopeLeft = self._fHPL
    #     self.pier._fSlopeRight = self._fHPR
    #     pass


class SpanCollection(list):
    def __init__(self, align_dict: dict, bridge_dict: dict):
        super().__init__()
        self.align_dict = align_dict
        self.bridge_dict = bridge_dict

    def add(self, s: Span = None, align: Align = None, bridge: Bridge = None, station: float = None,
            ang_deg: float = None) -> Span:
        if s != None:
            res = s
        elif align != None and bridge != None:
            res = Span(align, bridge, station, Angle.from_degrees(ang_deg).to_rad())
        else:
            raise Exception("参数不足.")
        self.append(res)
        self.sort()
        return res

    def read_csv(self, csv_path, sep=','):
        data = loadtxt(csv_path, delimiter=sep, dtype=str)
        for line in data:
            self.append(Span(self.align_dict[line[0]],
                             self.bridge_dict[line[1]],
                             float(line[2]),
                             Angle.from_degrees(line[3]).to_rad()
                             ))
        self.sort()

    def __getitem__(self, item) -> Span:
        return super(SpanCollection, self).__getitem__(item)


class Model(object):
    '''
    基础模型
    '''

    def __init__(self):
        self.alignments = {}
        self.bridges = {}
        self.spans = SpanCollection(self.alignments, self.bridges)

    def add_align(self, alignment: Align) -> int:
        """
        导入路线数据。

        Args:
            alignment: 路线对象

        Returns:
            int: 成功时返回 0，失败返回 -1
        """

        try:
            self.alignments[alignment.name] = alignment
            return 0
        except Exception as e:
            print(e)
            return -1

    def add_bridge(self, bri: Bridge) -> int:
        """
        导入桥梁数据。

        Args:
            bri (Bridge): 桥梁对象

        Returns:
            int : 成功时返回 0，失败返回 -1

        """
        try:
            self.bridges[bri.name] = bri
            return 0
        except Exception as e:
            print(e)
            return -1

    def add_span(self, spa: Span) -> int:
        try:
            self.spans.append(spa)
            self.spans.sort()
            spa.bridge.spanlist.append(spa)
            return 0
        except Exception as e:
            print(e)
            return -1

    def _project_xml(self) -> Document:
        """
        生成project.xml

        Returns:
            Document :  <class 'xml.dom.minidom.Document'>

        """
        doc = Document()
        pro = doc.createElement('project')
        brs = doc.createElement('bridges')
        als = doc.createElement('alignments')

        for key in self.alignments.keys():
            align = self.alignments[key]
            al = doc.createElement('alignment')
            al.setAttribute("name", align.name)
            file = doc.createElement("fileLocation")
            file.appendChild(doc.createTextNode(align._work_dir))
            al.appendChild(file)
            als.appendChild(al)
        for key in self.bridges.keys():
            bri = self.bridges[key]
            br = doc.createElement('bridge')
            br.setAttribute("name", bri.name)
            brs.appendChild(br)
        doc.appendChild(pro)
        pro.appendChild(als)
        pro.appendChild(brs)
        include = doc.createElement("include")
        include.appendChild(doc.createTextNode("./spans.xml"))
        pro.appendChild(include)
        return doc

    def _make_span_xml(self) -> Document:
        doc = Document()

        return doc

    def save_srb(self, filename):
        CLEANTMPS = True
        tmp, ex = os.path.splitext(filename)
        file = tmp + '.srb'
        z = zipfile.ZipFile(file, 'w', zipfile.ZIP_DEFLATED)

        proj_doc = self._project_xml()
        fpath = os.path.dirname(filename) + "/project.xml"
        with open(fpath, 'wb') as f:
            f.write(proj_doc.toprettyxml(indent='\t', encoding='utf-8'))

        z.write(fpath)
        if CLEANTMPS:
            os.remove(fpath)

        span_doc = self._make_span_xml()
        fpath = os.path.dirname(filename) + "/span.xml"
        with open(fpath, 'wb') as f:
            f.write(span_doc.toprettyxml(indent='\t', encoding='utf-8'))
        z.write(fpath)
        if CLEANTMPS:
            os.remove(fpath)
        z.close()

    def save_sql(self, connect):
        engine = create_engine(connect, echo=False)
        event.listen(engine, "before_cursor_execute", add_own_encoders)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        for al in self.alignments.keys():
            session.add(self.alignments[al])
        session.commit()
        for br in self.bridges.keys():
            session.add(self.bridges[br])
        session.commit()
        for sp in self.spans:
            session.add(sp)
            if sp.pier is not None:
                session.add(sp.pier.Sub_Inst)  # 添加下部结点
                session.add(sp.pier.CapBeam_Inst)  # 添加下部盖梁
                for col in sp.pier.ColumnList:  # 添加墩柱
                    session.add(col)
            if sp.foundation is not None:
                session.add(sp.foundation.Found_Inst)
                for pc in sp.foundation.PileCapList:
                    session.add(pc)
                for pile in sp.foundation.PileList:
                    session.add(pile)
        session.commit()
        for br in self.bridges.keys():
            for cip in self.bridges[br].ciplist:
                session.add(cip)
                for kp in cip.KeyPointsList:
                    session.add(kp)
        session.commit()


def add_own_encoders(conn, cursor, query, *args):
    # try:
    #     cursor.connection.encoders[np.float64] = lambda value, encoders: float(value)
    pass
