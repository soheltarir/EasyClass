from easy_class import EasyClass, IntegerVariable, StringVariable, PositiveIntegerVariable, \
    BooleanVariable, ClassVariable, DictVariable, DateTimeVariable, DateVariable, TimeVariable, EasyChoices


def test_definition():
    # Test for correct default value type
    try:
        class TestClass(EasyClass):
            var = BooleanVariable(default=4)
    except AttributeError:
        class TestClass(EasyClass):
            var = BooleanVariable(default=False)

    # Test correct choices
    try:
        class TestClass(EasyClass):
            var = IntegerVariable(choices="A")
    except AssertionError:
        class TestClass(EasyClass):
            choices = [1, 4, 6]
            var = IntegerVariable(choices=choices)

    try:
        class TestClass(EasyClass):
            choices = ["a", "b"]
            var = IntegerVariable(choices=choices)
    except AttributeError:
        class TestClass(EasyClass):
            choices = [0, 1]
            var = IntegerVariable(choices=choices)


def test_variable():
    class TestClass(EasyClass):
        a = StringVariable(null=False)
    try:
        TestClass()
    except ValueError:
        try:
            TestClass(a=1)
        except TypeError:
            TestClass(a="test")

    try:
        obj = TestClass(a="test")
        obj.a = None
    except ValueError:
        pass


def test_max_min():
    class TestClass(EasyClass):
        a = IntegerVariable(max_value=10, min_value=-10)
        b = StringVariable(max_length=5, min_length=2)
    obj = TestClass()
    try:
        obj.a = 11
    except ValueError:
        try:
            obj.a = -11
        except ValueError:
            obj.a = 5

    try:
        obj.b = "Test Variable"
    except ValueError:
        try:
            obj.b = "a"
        except ValueError:
            obj.b = "Test"


class test_positive():
    try:
        class TestClass(EasyClass):
            a = PositiveIntegerVariable(min_value=-1)
    except AttributeError:
        class TestClass(EasyClass):
            a = PositiveIntegerVariable(min_value=1)
    try:
        class TestClass(EasyClass):
            a = PositiveIntegerVariable(include_zero=False, min_value=0)
    except AttributeError:
        class TestClass(EasyClass):
            a = PositiveIntegerVariable(include_zero=False, min_value=2)

    class TestClassA(EasyClass):
        a = PositiveIntegerVariable(include_zero=False, min_value=2)
    obj = TestClass()
    try:
        obj.a = 1
    except ValueError:
        obj.a = 3


def test_date_time():
    class TestClass(EasyClass):
        a = DateTimeVariable()
        b = DateVariable()
        c = TimeVariable()

    obj = TestClass()
    try:
        obj.a = "Test"
    except ValueError:
        obj.a = "2016-01-01T00:00:00"
    try:
        obj.b = "Test"
    except ValueError:
        obj.b = "2016-01-01"
    try:
        obj.c = "Test"
    except ValueError:
        obj.c = "12:00:00"


def test_class_variable():
    class A(object):
        pass

    class TestClass(EasyClass):
        a = ClassVariable(cls=A)
    obj = TestClass()
    try:
        obj.a = 1
    except TypeError:
        obj.a = A()


def test_choice_variable():
    class TestClass(EasyClass):
        choices = [1, 2, 5]
        a = IntegerVariable(choices=choices)
    obj = TestClass()
    try:
        obj.a = 3
    except ValueError:
        obj.a = 1


def test_editable():
    class TestClass(EasyClass):
        a = DictVariable(default={"A": "B"}, editable=False)
    obj = TestClass()
    try:
        obj.a = {"K": "V"}
    except AssertionError:
        pass


def test_choices():
    class TestChoices(EasyChoices):
        a = (0, "A")
        b = (1, )

    class TestChoicesChild(TestChoices):
        c = (2, "c")

    print(TestChoicesChild.c)
