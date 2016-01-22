from datetime import datetime

from easy_class import EasyClass, IntegerVariable, StringVariable, PositiveIntegerVariable, FloatVariable, \
    BooleanVariable, ClassVariable, DictVariable, DateTimeVariable, DateVariable, TimeVariable


class SomeClass(object):
    var = 1

try:
    class TestClass(EasyClass):
        a = IntegerVariable(max_value=10, min_value=-10)
        b = StringVariable(null=False)
        c = PositiveIntegerVariable()
        d = FloatVariable(max_value=0.5, min_value=0.1)
        e = BooleanVariable(default=4)
        f = ClassVariable(cls=SomeClass)
        g = DictVariable(default={"name": "Test"}, editable=False)
        h = DateTimeVariable()
        i = DateVariable()
        j = TimeVariable()
except AttributeError:
    try:
        class TestClass(EasyClass):
            a = IntegerVariable(max_value=10, min_value=-10)
            b = StringVariable(null=False)
            c = PositiveIntegerVariable()
            d = FloatVariable(max_value=0.5, min_value=0.1)
            e = BooleanVariable(default=False)
            f = ClassVariable(cls=SomeClass)
            g = DictVariable(default={"name": "Test"}, editable=False)
            h = DateTimeVariable()
            i = DateVariable()
            j = TimeVariable()
            k = IntegerVariable(choices="A")
    except AssertionError:
        class TestClass(EasyClass):
            some_choices = [1, 4, 6]
            a = IntegerVariable(max_value=10, min_value=-10)
            b = StringVariable(null=False)
            c = PositiveIntegerVariable()
            d = FloatVariable(max_value=0.5, min_value=0.1)
            e = BooleanVariable(default=False)
            f = ClassVariable(cls=SomeClass)
            g = DictVariable(default={"name": "Test"}, editable=False)
            h = DateTimeVariable()
            i = DateVariable()
            j = TimeVariable()
            k = IntegerVariable(choices=some_choices)


def runtests():
    try:
        obj = TestClass()
    except ValueError:
        obj = TestClass(b="Testing")
    try:
        obj.b = None
    except AttributeError:
        pass
    try:
        obj.a = 11
    except ValueError:
        try:
            obj.a = -11
        except ValueError:
            obj.a = 5
    try:
        obj.c = -1
    except ValueError:
        obj.c = 1
    try:
        obj.d = 0.6
    except ValueError:
        try:
            obj.d = 0.05
        except ValueError:
            obj.d = 0.3
    try:
        obj.f = "Class"
    except TypeError:
        obj.f = SomeClass()
    obj.h = datetime(2016, 2, 1, hour=12)
    obj.i = '2016-02-01'
    obj.j = '12:00:00'
    try:
        obj.k = 7
    except ValueError:
        obj.k = 4
    try:
        obj.g = {"k": "v"}
    except AssertionError:
        pass


if __name__ == '__main__':
    runtests()
