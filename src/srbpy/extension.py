from PyAngle import Angle
from ezdxf.math import ConstructionLine, Vec2, ConstructionArc, ConstructionCircle
from skspatial.objects import Vector
from numpy import sqrt, arctan2, pi
import ezdxf


def rotate2d(vec: Vector, ang: Angle):
    x = vec[0] * ang.cos() - vec[1] * ang.sin()
    y = vec[0] * ang.sin() + vec[1] * ang.cos()
    if vec.dimension == 3:
        return Vector([x, y, vec[3]])
    else:
        return Vector([x, y])


def length(vec: Vector) -> float:
    if vec.dimension == 3:
        return sqrt(vec[0] ** 2 + vec[1] ** 2 + vec[2] ** 2)
    else:
        return sqrt(vec[0] ** 2 + vec[1] ** 2)


def intersection_seg_arc(h, k, r, x0, y0, x1, y1):
    """
    求线段和圆弧的交点

    Returns:
        (float,float) : 交点坐标

    """
    a = (x1 - x0) * (x1 - x0) + (y1 - y0) * (y1 - y0)
    b = 2 * (x1 - x0) * ((x0 - h)) + 2 * (y1 - y0) * (y0 - k)
    c = (x0 - h) * (x0 - h) + (y0 - k) * (y0 - k) - r * r
    # t1, t2;
    res = []
    if b * b - 4 * a * c < 0:
        return None
    else:
        t1 = (-b + sqrt(b * b - 4 * a * c)) / (2 * a)
        t2 = (-b - sqrt(b * b - 4 * a * c)) / (2 * a)
    if t1 >= 0 and t1 <= 1:
        res.append((x1 - x0) * t1 + x0)
        res.append((y1 - y0) * t1 + y0)
    if t2 >= 0 and t2 <= 1:
        res.append((x1 - x0) * t2 + x0)
        res.append((y1 - y0) * t2 + y0)
    return res


def signed_angle_between(from_v: Vec2, to_v: Vec2, return_neg: bool = False):
    """
    考虑符号的矢量夹角

    Args:
        from_v: 起始矢量
        to_v: 终止矢量
        returnNegative: 是否返回负值，默认FALSE

    Returns:
        float: 返回夹角弧度值，逆时针为正, 值域[0,2pi]

    """
    res = arctan2(to_v.normalize().y, to_v.normalize().x) - arctan2(from_v.normalize().y, from_v.normalize().x)
    if return_neg:
        return res
    else:
        if res < 0:
            return 2 * pi + res
        else:
            return res


def get_point_angle(cc: ConstructionCircle, x: float, y: float):
    """
    任意点到圆cc的连线与x轴的夹角
    Args:
        cc: 圆
        x: 点x坐标
        y: 点y坐标

    Returns:
        float: 弧度夹角，从x轴逆时针转动到连线
    """
    v1 = Vec2([x, y]) - cc.center
    v0 = Vec2([1, 0])
    return signed_angle_between(v0, v1)


def intersection(master: ConstructionLine, slaver: ConstructionArc):
    res = intersection_seg_arc(slaver.center.x, slaver.center.y, slaver.radius, master.start.x, master.start.y, master.end.x, master.end.y)
    if res == None or len(res) == 0:
        return None
    elif len(res) == 2:
        tmp = ConstructionCircle(slaver.center, slaver.radius)
        IntPointAng = Angle.from_rad(get_point_angle(tmp, res[0], res[1])).to_degrees()
        if slaver.start_angle <= slaver.end_angle and (slaver.start_angle <= IntPointAng and IntPointAng <= slaver.end_angle):
            return res[0], res[1]
        elif slaver.end_angle <= slaver.start_angle and not (slaver.end_angle <= IntPointAng and IntPointAng <= slaver.start_angle):
            return res[0], res[1]
    else:
        tmp = ConstructionCircle(slaver.center, slaver.radius)
        IntPointAng = Angle.from_rad(get_point_angle(tmp, res[0], res[1])).to_degrees()
        if slaver.start_angle <= slaver.end_angle and (slaver.start_angle <= IntPointAng and IntPointAng <= slaver.end_angle):
            return res[0], res[1]
        elif slaver.end_angle <= slaver.start_angle and not (slaver.end_angle <= IntPointAng and IntPointAng <= slaver.start_angle):
            return res[0], res[1]

        IntPointAng = Angle.from_rad(get_point_angle(tmp, res[2], res[3])).to_degrees()
        if slaver.start_angle <= slaver.end_angle and (slaver.start_angle <= IntPointAng and IntPointAng <= slaver.end_angle):
            return res[2], res[3]
        elif slaver.end_angle <= slaver.start_angle and not (slaver.end_angle <= IntPointAng and IntPointAng <= slaver.start_angle):
            return res[2], res[3]
    return None


def cut_dxf(dxf_file, center: Vector, side: Vector):
    """
    切割dxf文件.

    Args:
        dxf_file: dxf文件路径, R12格式推荐.
        center: 切割线起点
        side: 切割线终点

    Returns:
        (float, Vector) : 交点至起点距离, 交点坐标. 如无交点则返回 None,None.

    """
    cutLine = ConstructionLine(center, side)
    pts = []
    doc = ezdxf.readfile(dxf_file)
    msp = doc.modelspace()
    for e in msp:
        if e.dxftype() == 'LINE':
            byLine = ConstructionLine(e.dxf.start, e.dxf.end)
            pt = cutLine.intersect(byLine)
            if isinstance(pt, Vec2):
                pts.append(pt)
        elif e.dxftype() == 'ARC':
            byArc = ConstructionArc(e.dxf.center, e.dxf.radius, e.dxf.start_angle, e.dxf.end_angle)
            coord = intersection(cutLine, byArc)
            if coord != None:
                pt = Vec2(*coord)
                pts.append(pt)

    if len(pts) != 0:
        pts.sort(key=lambda x: x.distance(center))
        return pts[0].distance(center), pts[0]
    else:
        return None, None


if __name__ == "__main__":
    arctan2(1, 1)
