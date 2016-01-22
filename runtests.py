from datetime import datetime

from easy_class import EasyClass, IntegerVariable, StringVariable, PositiveIntegerVariable, FloatVariable, \
    BooleanVariable, ClassVariable, DictVariable, DateTimeVariable, DateVariable, TimeVariable


class SomeClass(object):
    var = 1


class TestClass(EasyClass):
    a = IntegerVariable(max_value=10, min_value=-10)
    b = StringVariable(null=False)
    c = PositiveIntegerVariable()
    d = FloatVariable()
    e = BooleanVariable(default=False)
    f = ClassVariable(cls=SomeClass)
    g = DictVariable(default={"name": "Test"}, editable=False)
    h = DateTimeVariable()
    i = DateVariable()
    j = TimeVariable()


def runtests():
    obj = TestClass(b="Testing")
    obj.a = 5
    obj.c = 1
    obj.d = 0.2
    obj.f = SomeClass()
    obj.h = datetime(2016, 2, 1, hour=12)
    obj.i = '2016-02-01'
    obj.j = '12:00:00'


if __name__ == '__main__':
    runtests()
