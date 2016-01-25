from future.utils import with_metaclass


class Choice(object):
    def __init__(self, value, label=None):
        self.value = value
        self.label = label

    def __get__(self, instance, owner):
        return self.value


class Labels(dict):
    def __getattribute__(self, name):
        result = dict.get(self, name, None)
        if result is not None:
            return result
        else:
            raise AttributeError("Label for field %s was not found." % name)

    def __setattr__(self, name, value):
        self[name] = value


class EasyChoiceMeta(type):
    def __new__(cls, name, bases, attrs):
        choices = {}
        labels = Labels()
        values = []

        # Get all the attributes from parent classes.
        parents = [b for b in bases if isinstance(b, EasyChoiceMeta)]
        for kls in parents:
            for choice_name in kls._choices:
                choices[choice_name] = kls._choices[choice_name]

        # Get all the attributes from current class.
        for choice_name, val in attrs.items():
            if isinstance(val, tuple):
                choices[choice_name] = val

        for choice_name, val in choices.items():
            values.append(val[0])
            try:
                label = val[1]
            except IndexError:
                label = choice_name.lower()
            setattr(labels, choice_name, label)
            attrs[choice_name] = Choice(value=val[0], label=label)

        attrs["_choices"] = choices
        attrs["values"] = choices.values()
        attrs["choices"] = values
        attrs["labels"] = labels

        return super(EasyChoiceMeta, cls).__new__(cls, name, bases, attrs)


class EasyChoices(with_metaclass(EasyChoiceMeta, object)):
    choices = []
    labels = Labels()
