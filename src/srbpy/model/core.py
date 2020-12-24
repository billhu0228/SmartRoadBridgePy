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
from ..stdlib.std_piers import PierBase
from xml.dom.minidom import Document
from ..alignment.align import Align
from ..server import Base, Column, String, Text, ForeignKey, relationship, Float, FLOAT, DECIMAL
from ezdxf.math import Vec2, Matrix44, Vector


class Bridge(Base):
    __tablename__ = "bridge_tbl"
    name = Column('name', String(10), primary_key=True)
    _f_ali_name = Column('align_name', String(10), ForeignKey("ei_tbl.name", ondelete='CASCADE', onupdate='CASCADE'))
    _f_title_name = Column('title_name', String(120), nullable=True)
    _align_related = relationship("Align", foreign_keys=[_f_ali_name], cascade='save-update,delete')

    def __init__(self, name: str, al: Align):
        self.name = name
        self._align_related = al

    def set_title(self, title: str):
        self._f_title_name = title

    def serialize(self):
        return json.dumps({"name": self.name})


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
        return self._fName

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

    def assign_found2(self, inst_name: str, fund_inst: Base,
                      off_l: float = 0, off_w: float = 0, off_h: float = 0,
                      angle_deg: float = 0):

        self.foundation = fund_inst.copy()
        self.foundation.Found_Inst.Name = inst_name
        self.foundation.Found_Inst.RelatedSpan = self
        for ii, pile in enumerate(self.foundation.PileList):
            pile.Name = inst_name + "/PI%s" % str(ii + 1).zfill(2)
        for ii, pc in enumerate(self.foundation.PileCapList):
            pc.Name = inst_name + "/PC%s" % str(ii + 1).zfill(2)
        span_cc = Vector(self.align.get_coordinate(self.station))
        span_cc._z = self.align.get_ground_elevation(self.station, 0)
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

    def assign_pier(self, name_inst: str, pier_inst: PierBase):
        """
        指定属于本处分跨线的桥墩结构实例.

        Args:
            name: 桥墩编号.
            pier_inst: 桥墩实例.

        Returns:

        """
        self.pier = copy.deepcopy(pier_inst)
        self.pier._fName = name_inst
        self.pier.align = self.align
        self.pier.bridge = self.bridge
        self.pier.span = self
        self.pier._fStation = self._fStation
        self.pier._fAngle = self._fAngle
        self.pier._fSlopeLeft = self._fHPL
        self.pier._fSlopeRight = self._fHPR
        pass


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
                session.add(sp.pier)
            if sp.foundation is not None:
                session.add(sp.foundation.Found_Inst)
                for pc in sp.foundation.PileCapList:
                    session.add(pc)
                for pile in sp.foundation.PileList:
                    session.add(pile)
        session.commit()


def add_own_encoders(conn, cursor, query, *args):
    # try:
    #     cursor.connection.encoders[np.float64] = lambda value, encoders: float(value)
    pass
