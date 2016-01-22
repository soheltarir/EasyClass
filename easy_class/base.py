from future.utils import with_metaclass

from .fields import Variable
from .meta import EasyClassMeta


class EasyClass(with_metaclass(EasyClassMeta, object)):
    def __repr__(self):
        return "<{0}: {1}>".format(self.__class__.__name__, vars(self).get('__str__', None))

    def __init__(self, **kwargs):
        defined_attributes = [x for x, y in vars(self.__class__).items() if issubclass(y.__class__, Variable)]
        non_kwarg_attributes = [x for x in defined_attributes if x not in kwargs]
        for key, value in kwargs.items():
            setattr(self, key, value)
        for attr in non_kwarg_attributes:
            vars(self)[attr] = vars(self.__class__)[attr].default
        self.check_nullable()
        super(EasyClass, self).__init__()

    def check_nullable(self):
        non_null_attributes = [
            key for key, value in vars(self.__class__).items()
            if issubclass(value.__class__, Variable) and value.null is False and getattr(self, key, None) is None
            ]
        if len(non_null_attributes):
            raise ValueError("Following attributes cannot be null: [{0}]".format(", ".join(non_null_attributes)))
