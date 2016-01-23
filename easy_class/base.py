from future.utils import with_metaclass

from .fields import Variable


class EasyClassMeta(type):
    def __new__(cls, name, bases, attrs):
        attributes = {}

        if "_attribute" in attrs:
            raise NameError("_attribute is a reserved attribute name, please use a different name.")

        # Get all the attributes from parent classes.
        parents = [b for b in bases if isinstance(b, EasyClassMeta)]
        for kls in parents:
            for attr_name in kls._attributes:
                attributes[attr_name] = kls._attributes[attr_name]

        # Get all the attributes from current class.
        for attr_name, val in attrs.items():
            if issubclass(val.__class__, Variable):
                attributes[attr_name] = val
        for attribute, val in attributes.items():
            if attribute not in attrs:
                # This means this a parent class attribute
                attrs[attribute] = val
            attrs[attribute].name = attribute
        attrs['_attributes'] = attributes

        return super(EasyClassMeta, cls).__new__(cls, name, bases, attrs)


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
