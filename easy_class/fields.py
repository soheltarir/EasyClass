class Variable(object):
    def __init__(self, name=None, default=None, null=True, value_type=None, choices=None):
        self.name = name
        self.default = default
        self.null = null
        self.type = value_type
        if choices:
            assert isinstance(self.choices, list), \
                "choices expects list type, but received {0}".format(type(choices).__name__)
        self.choices = choices

    def base_setter_checks(self, value):
        if self.null is False and value is None:
            raise ValueError("{0} cannot be null".format(self.name))
        if not isinstance(value, self.type):
            raise TypeError("{0} expects {1} type, but received {2}.".
                            format(self.name, self.type.__name__, type(value).__name__)
                            )
        if self.choices and value not in self.choices:
            raise ValueError("Value should be among [{0}]".format(", ".join(self.choices)))

    def __get__(self, instance, owner):
        value = vars(instance).get(self.name, self.default)
        if self.null is False and value is None:
            raise AttributeError("{0} cannot be null".format(self.name))
        return value

    def __set__(self, instance, value):
        self.base_setter_checks(value)
        vars(instance)[self.name] = value

    def __delete__(self, instance):
        raise AttributeError("Can't delete attribute")


class IntegerVariable(Variable):
    def __init__(self, **kwargs):
        super(IntegerVariable, self).__init__(**kwargs)
        self.type = int


class StringVariable(Variable):
    def __init__(self, **kwargs):
        self.max_length = kwargs.pop('max_length', 255)
        self.min_length = kwargs.pop('min_length', 0)
        super(StringVariable, self).__init__(**kwargs)
        self.type = str

    def setter_checks(self, value):
        if len(value) > self.max_length:
            raise ValueError("Length of \"{0}\" for attribute {1} exceeds max_length specified of {2}".
                             format(value, self.name, self.max_length))
        if len(value) < self.min_length:
            raise ValueError("Length of \"{0}\" for attribute {1} is less than min_length specified of {2}".
                             format(value, self.name, self.min_length))

    def __set__(self, instance, value):
        self.setter_checks(value)
        super(StringVariable, self).__set__(instance, value)
