import os
import zipfile

from PyAngle import Angle
from numpy import loadtxt
from xml.dom.minidom import Document
from srbpy.alignment.align import Align


class Bridge(object):
    def __init__(self, name: str):
        self.name = name


class Span(object):
    """
    跨径线类



    """

    def __init__(self, align: Align, bridge: Bridge, station: float, angle: float):
        self.align = align
        self.bridge = bridge
        self.station = station
        self.angle = angle
        self.pier = None
        self.foundation = None
        self.mj = None

    def __str__(self):
        return self.align.name + "+%.3f".zfill(7) % self.station

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
        return Span(self.align, self.station + dist, self.angle)

    def __sub__(self, other) -> float:
        if isinstance(other, Span):
            if other.align == self.align:
                return self.station - other.station
            else:
                print("警告：桩号不在同一条设计线")
                return self.station - other.station
        raise Exception("无法与其他类型相减.")


class SpanCollection(list):
    def __init__(self, align_dict: dict, bridge_dict: dict):
        super().__init__()
        self.align_dict = align_dict
        self.bridge_dict = bridge_dict

    def add(self, s: Span = None, align: Align = None, bridge: Bridge = None, station: float = None, ang_deg: float = None) -> Span:
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

    def load_align(self, path: str, name: str = ""):
        """
        导入路线数据。

        Args:
            path: 路线数据包
            name:  optional, 路线名称，如为空则使用数据表文件

        Returns:
            Align: 路线实例
        """

        a1 = Align(path, name)
        self.alignments[a1.name] = a1
        return a1

    def load_bridge(self, obj: Bridge):
        if not obj.name in self.bridges.keys():
            self.bridges[obj.name] = obj

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
        tmp,ex = os.path.splitext(filename)
        file=tmp+'.srb'
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
