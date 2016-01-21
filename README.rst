EASY Class
==========

EASY Class is a toolkit for creating generic classes in an elegant way.

## Usage
--------
```python
from easy_class import EasyClass, StringVariable, IntegerVariable


class MyClass(EasyClass):
    attr1 = IntegerVariable()
    attr2 = StringVariable()
```
The above code declares a class with two member variables **attr1** and **attr2**, where **attr1** can only be an integer value and **attr2** can only be a string. Hence, if you try to do the following
```python
obj = MyClass()
obj.attr1 = "Test"
```
it will raise the exception `TypeError: attr1 expects int type, but received str.`

## Class Variable Reference
---------------------------
All Variable types (i.e. IntegerVariable, StringVariable) are inherited from the class **Variable** which represents a class attribute type. Below contains all the API references of **Variable** including the variable options and field types this package offers.

### Variable options
The following arguments are available to all variable types. All are optional.
## null
#### Variable.null
If **False** the attribute cannot be assigned a **NULL** variable. Default is **True**. You cannot also instantiate a class which has any Non-nullable attributes without specifying the correct arguments. Below is what I meant to say.
```python
class MyClass(EasyClass):
    attr1 = IntegerVariable(null=False)
    attr2 = StringVariable(null=False)

obj = MyClass()
```
The above will raise the exception `ValueError: Following attributes cannot be null: [attr2, attr1]`

## choices
#### Variable.choices
A list to use as choices for the attribute. Will raise exception if value being is stored is not included in this list of choices.

## default
#### Variable.default
The default value for the attribute. Right now, callables are not supported.

-----
### Variable Types

## IntegerVariable
An Integer Variable

## StringVariable
A string variable, for small- to large-sized strings.
**StringVariable** has the following extra arguments
#### StringVariable.max_length
The maximum length (in characters) of the attribute. Defaults **255**.
#### StringVariable.min_length
The minimum length (in characters) of the attribute. Defaults **0**.
