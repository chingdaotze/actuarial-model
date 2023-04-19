.. _tutorial_pt3:

Tutorial, Part 3
================

Object Model in Practice
------------------------

We can use the modeling framework by inheriting from the :ref:`object model <object_model>` and creating
custom data sources, projection entities, projection values, and projections.

In the next few sections, we'll see how this works with the sample annuity model.

.. collapse:: About inheritance...

    `Inheritance <https://en.wikipedia.org/wiki/Inheritance_(object-oriented_programming)>`_
    is a mechanism where classes can have defined hierarchical relationships with other classes.

    For example, in our previous note on :ref:`classes <classes_note>`, we defined an ``Account`` class
    which models a bank account:

    .. code-block:: python

        class Account:

            _balance: float

            def __init__(
                self
            ):

                self._balance = 0.0

            def deposit(
                self,
                amount: float
            ) -> None:

                self._balance += amount

    Now suppose we want to define a special type of account that provides a 5% bonus on every deposit.
    We can declare a new "bonus" ``Account`` class, derived from our original ``Account`` class like so:

    .. code-block:: python

        class BonusAccount(
            Account  # "BonusAccount" is derived from "Account"
        ):

            _bonus_rate: float

            def __init__(
                self
            ):

                self._bonus_rate = 0.05

            def deposit(
                self,
                amount: float
            ) -> None:

                self._balance += amount * (1.0 + self._bonus_rate)

    Note that:

    #. We **inherit** all attributes from the **super class**. In this example, the super class is
       ``Account``, and we've inherited the ``_balance`` and ``deposit`` attributes.

    #. We've declared a new ``_bonus_rate`` attribute, that only exists in ``BonusAccount`` objects
       (and *not* in ``Account`` objects).

       .. _inheritance_override:

    #. We've **overridden** the definition of the ``deposit`` function. The behavior of ``deposit``
       changes depending on whether the object is an ``Account`` or a ``BonusAccount``.

    Using inheritance, we can:

    #. Minimize code re-use by inheriting code that is common between classes.
    #. Extend the functionality of existing classes.
    #. Change the functionality in existing classes.

Annuity Model Design and Construction
-------------------------------------

Walk through code base.

Data Sources
^^^^^^^^^^^^

#. Create Root Data Sources.

#. Decide on input format.

#. Create a new Data Source type, if it doesn't already exist.

#. Inherit the Data Source type.

#. Define interfaces.

#. Add to Data Sources

Projection Entities
^^^^^^^^^^^^^^^^^^^



Projection
^^^^^^^^^^


