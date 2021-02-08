# -*- coding : utf-8-*-
"""
SrbPy
=====

提供了两个子模块：
  1. 路线模块（srbpy.alignment），用于解析EICAD路线数据包并解析.
  2. 模型（srbpy.model），用于建模。

路线模块
----------------------------
EI路线数据类Align.

"""


from .align import Align

__all__ = [f for f in dir() if not f.startswith("_")]