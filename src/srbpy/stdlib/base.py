# -*- coding : utf-8-*-
import abc
from enum import Enum


class StructTypeEunm(Enum):
    Default = 0
    Foundation = 1
    Pier = 2
    Beam = 3
    MovementJoint = 4
    Bearing = 5


class StructTemplate(metaclass=abc.ABCMeta):
    """
    构造物模板的基类


    """

    def __init__(self, **kwargs):
        super().__init__()
        self.ParameterTable = {}
        self._REGISTERED_KEYWORDS = []
        self._register_kwd()
        if len(self._REGISTERED_KEYWORDS) == 0:
            raise Exception("%s未注册任何参数." % self.__class__.__name__)
        for key in kwargs.keys():
            if key in self._REGISTERED_KEYWORDS:
                self.ParameterTable[key] = kwargs[key]

    @abc.abstractmethod
    def _register_kwd(self):
        """
        注册参数的抽象方法, 构造函数调用一次, 子类定义中需实现. 已注册的参数可以在构造函数中使用.

        Returns:

        """
        pass

    @abc.abstractmethod
    def TypeID(self) -> StructTypeEunm:
        """
        注册结构类型

        Returns:

        """
        pass
