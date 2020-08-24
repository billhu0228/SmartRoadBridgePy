from ..alignment import Align


class Model(object):
    '''
    基础模型
    '''

    def __init__(self):
        self._alignments = {}

    def load_align(self, path: str, name: str = ""):
        '''
        导入路线数据
        :param path: 路线数据包
        :param name: optional, 路线名称，如为空则使用数据表文件
        :return: 无
        '''
        a1 = Align(path, name)
        self._alignments[a1.name] = a1
