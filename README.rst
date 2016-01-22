============================
EASY Class |package| |build|
============================

EASY Class is a toolkit for creating generic classes in an elegant way.

=====
Usage
=====

.. code:: python

    from easy_class import EasyClass, StringVariable, IntegerVariable


    class MyClass(EasyClass):
        attr1 = IntegerVariable()
        attr2 = StringVariable()

The above code declares a class with two member variables **attr1** and
**attr2**, where **attr1** can only be an integer value and **attr2**
can only be a string. Hence, if you try to do the following

.. code:: python

    obj = MyClass()
    obj.attr1 = "Test"

it will raise the exception ``TypeError: attr1 expects int type, but received str.``

========================
Class Variable Reference
========================

All Variable types (i.e. IntegerVariable, StringVariable) are inherited
from the class **Variable** which represents a class attribute type.
Below contains all the API references of **Variable** including the
variable options and field types this package offers.

----------------
Variable options
----------------

The following arguments are available to all variable types. All are
optional.

null
----
If **False** the attribute cannot
be assigned a **NULL** variable. Default is **True**. You cannot also
instantiate a class which has any Non-nullable attributes without
specifying the correct arguments. Below is what I meant to say.

.. code:: python

    class MyClass(EasyClass):
        attr1 = IntegerVariable(null=False)
        attr2 = StringVariable(null=False)

    obj = MyClass()

The above will raise the exception ``ValueError: Following attributes cannot be null: [attr2, attr1]``

choices
-------
A list to use as choices for the attribute. Will raise exception if
value being is stored is not included in this list of choices.

default
-------
The default value for the attribute. Right now, callables are not
supported.

editable
--------
If **False**, the attribute value cannot be edited. Default is **True**.

--------------
Variable Types
--------------

**IntegerVariable**
-------------------
An Integer Variable. **IntegerVariable** allows the following extra arguments.

max_value
~~~~~~~~~
The maximum value that can be set for the attribute. Default is **None** (i.e., no validation is done)

min_value
~~~~~~~~~
The minimum value that can be set for the attribute. Default is **None** (i.e., no validation is done)

**StringVariable**
------------------

A string variable, for small- to large-sized strings. **StringVariable**
has the following extra arguments

max_length
~~~~~~~~~~
The maximum length (in characters) of the attribute. Defaults **255**.

min_length
~~~~~~~~~~
The minimum length (in characters) of the attribute. Defaults **0**.

**BooleanVariable**
-------------------
A true/false attribute.

**FloatVariable**
-----------------
A floating-point number represented in Python by a **float** instance. **FloatVariable** accepts same arguments as an **IntegerField**.

**ClassVariable**
-----------------
A custom class variable. Required keyword argument ``cls`` must be passed to a **ClassVariable**. Below is an example.
 .. code:: python

    class A(object):
       pass

    class MyClass(EasyClass):
       a = ClassVariable(cls=A, null=False)

**DictVariable**
----------------
A dictionary variable.

**DateTimeVariable**
--------------------
A python **datetime** variable. **DateTimeVariable** either accepts a **datetime** variable or string of the
format ``YYYY-MM-DDTHH:MM:SS``.


**DateVariable**
----------------
A python **date** variable. **DateVariable** either accepts a **date** variable or string of the
format ``YYYY-MM-DD``.


**TimeVariable**
----------------
A python **time** variable. **TimeVariable** either accepts a **time** variable or string of the
format ``HH:MM:SS``.


.. |package| image:: https://badge.fury.io/py/easy-class.svg
                     :target: https://pypi.python.org/pypi/easy-class
.. |build| image:: https://travis-ci.org/soheltarir/EasyClass.svg?branch=master