from srbpy.stdlib.base import *


class OneColumnPier(StructTemplate):
    """
    独柱墩, 墩中心与设计线跨径线交点重合

    Keyword Args:
        section(str) : 例如输入"4*1.6", 可定义横桥向4m宽, 顺桥向1.6m厚的矩形断面独柱墩

    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def TypeID(self) -> StructTypeEunm:
        return StructTypeEunm.Pier

    def _register_kwd(self):
        self._REGISTERED_KEYWORDS = ["section"]


if __name__ == "__main__":
    C1 = OneColumnPier(section="4*1.6")
    t = 1
