from datetime import datetime, date, time

DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S'
DATE_FORMAT = '%Y-%m-%d'
TIME_FORMAT = '%H:%M:%S'


class Variable(object):
    def __init__(self, name=None, default=None, null=True, value_type=None, choices=None, editable=True):
        self.name = name
        self.default = default
        self.null = null
        self.type = value_type
        self.editable = editable
        if default is not None and not isinstance(default, value_type):
            raise AttributeError("Type mismatch for default value of {0}, expected {1}".
                                 format(self.__class__.__name__, self.type.__name__))
        if choices:
            assert isinstance(choices, list), \
                "choices expects list type, but received {0}".format(type(choices).__name__)
        self.choices = choices

    def base_setter_checks(self, value):
        if not self.editable:
            raise AssertionError("Attribute {0} is not editable".format(self.name))
        if self.null is False and value is None:
            raise ValueError("{0} cannot be null".format(self.name))
        if not isinstance(value, self.type):
            raise TypeError("{0} expects {1} type, but received {2}.".
                            format(self.name, self.type.__name__, type(value).__name__)
                            )
        if self.choices and value not in self.choices:
            raise ValueError("Value should be among '{0}'".format(self.choices))

    def __get__(self, instance, owner):
        value = vars(instance).get(self.name, self.default)
        if self.null is False and value is None:
            raise AttributeError("{0} cannot be null".format(self.name))
        return value

    def __set__(self, instance, value):
        self.base_setter_checks(value)
        if hasattr(self, "setter_checks"):
            method = getattr(self, "setter_checks")
            method(value)
        vars(instance)[self.name] = value

    def __delete__(self, instance):
        raise AttributeError("Can't delete attribute")


class IntegerVariable(Variable):
    def __init__(self, **kwargs):
        self.max_value = kwargs.pop('max_value', None)
        self.min_value = kwargs.pop('min_value', None)
        super(IntegerVariable, self).__init__(value_type=int, **kwargs)

    def setter_checks(self, value):
        if self.max_value and value > self.max_value:
            raise ValueError("{0} exceeds max_value of {1} specified".format(self.name, self.max_value))
        if self.min_value and value < self.min_value:
            raise ValueError("{0} less than min_value of {1} specified".format(self.name, self.min_value))

    def __set__(self, instance, value):
        self.setter_checks(value)
        super(IntegerVariable, self).__set__(instance, value)


class PositiveIntegerVariable(IntegerVariable):
    def __init__(self, **kwargs):
        self.include_zero = kwargs.pop('include_zero', True)
        super(PositiveIntegerVariable, self).__init__(**kwargs)
        if self.min_value:
            if self.include_zero and self.min_value < 0:
                raise AttributeError("min_value for a {0} cannot be less than 0".format(self.__class__.__name__))
            if not self.include_zero and self.min_value <= 0:
                raise AttributeError("min_value for a {0} cannot be less than or equal to 0".
                                     format(self.__class__.__name__))

    def setter_checks(self, value):
        if self.include_zero and value < 0:
            raise ValueError("{0}'s value cannot be less than 0".format(self.name))
        if not self.include_zero and value <= 0:
            raise ValueError("{0}'s value cannot be less than or equal to 0".format(self.name))
        super(PositiveIntegerVariable, self).setter_checks(value)


class FloatVariable(Variable):
    def __init__(self, **kwargs):
        self.max_value = kwargs.pop('max_value', None)
        self.min_value = kwargs.pop('min_value', None)
        super(FloatVariable, self).__init__(value_type=float, **kwargs)

    def setter_checks(self, value):
        if self.max_value and value > self.max_value:
            raise ValueError("{0} exceeds max_value of {1} specified".format(self.name, self.max_value))
        if self.min_value and value < self.min_value:
            raise ValueError("{0} less than min_value of {1} specified".format(self.name, self.min_value))

    def __set__(self, instance, value):
        self.setter_checks(value)
        super(FloatVariable, self).__set__(instance, value)


class StringVariable(Variable):
    def __init__(self, **kwargs):
        self.max_length = kwargs.pop('max_length', 255)
        self.min_length = kwargs.pop('min_length', 0)
        super(StringVariable, self).__init__(value_type=str, **kwargs)

    def setter_checks(self, value):
        if value and len(value) > self.max_length:
            raise ValueError("Length of \"{0}\" for attribute {1} exceeds max_length specified of {2}".
                             format(value, self.name, self.max_length))
        if value and len(value) < self.min_length:
            raise ValueError("Length of \"{0}\" for attribute {1} is less than min_length specified of {2}".
                             format(value, self.name, self.min_length))


class BooleanVariable(Variable):
    def __init__(self, **kwargs):
        super(BooleanVariable, self).__init__(value_type=bool, **kwargs)


class ClassVariable(Variable):
    def __init__(self, cls, **kwargs):
        super(ClassVariable, self).__init__(value_type=cls, **kwargs)


class DictVariable(Variable):
    def __init__(self, **kwargs):
        super(DictVariable, self).__init__(value_type=dict, **kwargs)


class DateTimeVariable(ClassVariable):
    def __init__(self, **kwargs):
        super(DateTimeVariable, self).__init__(cls=datetime, **kwargs)

    @staticmethod
    def clean_value(value):
        if isinstance(value, str):
            return datetime.strptime(value, DATETIME_FORMAT)
        else:
            return value

    def __set__(self, instance, value):
        super(DateTimeVariable, self).__set__(instance, self.clean_value(value))


class DateVariable(ClassVariable):
    def __init__(self, **kwargs):
        super(DateVariable, self).__init__(cls=date, **kwargs)

    @staticmethod
    def clean_value(value):
        if isinstance(value, str):
            return datetime.strptime(value, DATE_FORMAT).date()
        else:
            return value

    def __set__(self, instance, value):
        super(DateVariable, self).__set__(instance, self.clean_value(value))


class TimeVariable(ClassVariable):
    def __init__(self, **kwargs):
        super(TimeVariable, self).__init__(cls=time, **kwargs)

    @staticmethod
    def clean_value(value):
        if isinstance(value, str):
            return datetime.strptime(value, TIME_FORMAT).time()
        else:
            return value

    def __set__(self, instance, value):
        super(TimeVariable, self).__set__(instance, self.clean_value(value))
