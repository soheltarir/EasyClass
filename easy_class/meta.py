from .fields import Variable


class EasyClassMeta(type):
    def __call__(cls, *args, **kwargs):
        for attr in [key for key, value in vars(cls).items() if isinstance(value, Variable)]:
            vars(cls)[attr].name = attr
        return super(EasyClassMeta, cls).__call__(*args, **kwargs)
