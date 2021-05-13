# -*- coding : utf-8-*-
"""
SrbPy
=====

提供了两个子模块：
  1. 路线模块（srbpy.alignment），用于解析EICAD路线数据包并解析.
  2. 模型（srbpy.model），用于建模。

路线模块
----------------------------
首先导入路线对象

  >>> from srbpy.alignment import Align
  >>> m1k = Align(path ="xxx", name="m1k")

Align 类提供了若干支持路线查询的基本函数，例如通过里程桩号pk，获取中桩大地坐标、设计高程、地面高程、纵横坡等数据：

  >>> x,y = m1k.get_coordinate(pk=16000)
  >>> design_level = m1k.get_elevation(16000)
  >>> ground_level = m1k.get_ground_elevation(16000)
  >>> print(x, y)
  >>> 472736.5636194062 9854283.750879934

Align 类还支持根据坐标反查最近的正交桩号（可能有多解）：

  >>> pk = m1k.get_station_by_point(x0=472736.5636194062, y0=9854283.750879934)
  >>> print(pk)
  >>> 16000.000000000384


模型模块
---------------------
开发中..

标准库
---------
开发中..


"""





# Remove dunders
from .alignment import *
from .model import *
from .stdlib import *
from .server import *


__all__ = [f for f in dir() if not f.startswith("_")]

import requests
import json
try:
    from packaging.version import parse
except ImportError:
    from pip._vendor.packaging.version import parse

def get_version():
    """Return version of package on pypi.python.org using json."""
    URL_PATTERN = 'https://pypi.python.org/pypi/Srbpy/json'
    req = requests.get(URL_PATTERN)
    version = parse('0')
    if req.status_code == requests.codes.ok:
        try:
            j = json.loads(req.text.encode(req.encoding))
        except:
            j=json.loads(req.text.encode('utf-8'))
        releases = j.get('releases', [])
        for release in releases:
            ver = parse(release)
            if not ver.is_prerelease:
                version = max(version, ver)
    return version

import pkg_resources  # part of setuptools

version = pkg_resources.require("Srbpy")[0].version
version_online = get_version()

if version != version_online:
    print("\nSrbpy当前版本(%s)，请更新最新版（%s）."%(version,version_online))
