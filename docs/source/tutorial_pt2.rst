.. _tutorial_pt2:

Tutorial, Part 2
================

Directory Structure
-------------------

The modeling framework is self-contained and (once setup is complete) everything it needs can be found
within its own directory structure.

- **\\.idea**

  This directory contains various PyCharm project files. It serves two main functions:

  #. Indicates that this directory contains a PyCharm project, and can be opened in PyCharm as a project.
  #. Defines project parameters, including things like directory structure, interpreter options,
     run configurations, etc...

  .. note::
     If you've used *Visual Studio* before, this directory is analogous to *Visual Studio*'s *\*.msproj* file.

- **\\docs**

  Contains source files, images, and other resources used to compile :ref:`this documentation <home>`.

- **\\install**

  Contains the *requirements.txt* file, which contains a list of 3rd party Python module dependencies.
  The *requirements.txt* file can be :ref:`used by pip to install dependencies <required_packages>`.

- **\\log**

  Holds :ref:`log files <log_file>` for each model run, generated at runtime.

- **\\output**

  Holds :ref:`model output <model_output>`, generated at runtime.

- **\\resource**

  Holds model input files, like:

  * Model points
  * Economic scenarios
  * Model assumptions

- **\\src**

  This is the meat and potatoes of the modeling framework. It contains:

  * Modeling framework logic and source code.
  * Models and model logic built on top of the modeling framework.

- **\\venv**

  Contains the Python virtual environment created in :ref:`step 5 <virtual_environment>` of the installation
  instructions.

.. _object_model:

Object Model
------------

The modeling framework consists of four core building blocks, built using classes:

.. graphviz::

    digraph {
        edge [dir="back"];
        node [fontname="Arial", shape="Box"];

        "(4) Projection" -> "(2) Projection Entity";
        "(3) Projection Values" -> "(1) Data Sources" [style=dashed];
        "(2) Projection Entity" -> "(1) Data Sources" [style=dashed];
        "(2) Projection Entity" -> "(3) Projection Values";
    }

.. _classes_note:

.. collapse:: About classes...

    The Object Model is implemented in Python using
    `classes <https://en.wikipedia.org/wiki/Class_(computer_programming)>`_.
    Classes are programming constructs that serve as *blueprints* for
    `objects <https://en.wikipedia.org/wiki/Object_(computer_science)>`_.

    Here's a simple class that models a bank account:

    .. code-block:: python
        :linenos:

        class Account:

            _balance: float  # Declare the data type for the "_balance" attribute

            def __init__(
                self
            ):

                self._balance = 0.0  # Declare the "_balance" attribute and set the initial value to zero

            def deposit(
                self,
                amount: float
            ) -> None:

                self._balance += amount  # Increment the "_balance" attribute by the "amount"

    The *Account* class consists of two **attributes**:

    #. Line 9, ``_balance`` - An account balance.
    #. Line 11, ``deposit`` - A function (or **method**) called ``deposit`` that increases the ``_balance``
       by a given ``amount``.

    Note that the class is a *blueprint* for an object. To use the class, we have to create an
    `instance <https://en.wikipedia.org/wiki/Instance_(computer_science)>`_ of the class. For example:

    .. code-block:: python

        chase_account = Account()
        wells_fargo_account = Account()
        bank_of_america_account = Account()

    In the code block above, we've created three different accounts using the ``Account`` blueprint,
    where each account can maintain and track its own balance. The difference between a class and an
    instance is analogous to the difference between a blueprint of a house and an actual, physical
    house. One blueprint may yield many different houses.

    Once we've created an instance, we can access attributes using "dot" notation. For example, to
    call the ``deposit`` method and deposit $500.00 to the Chase account:

    .. code-block:: python

        chase_account.deposit(
            amount=500.0
        )

    Lastly, some additional notes on classes:

    .. _constructor_note:

    #. The
       `__init__ <https://docs.python.org/3/tutorial/classes.html#class-objects>`_ method in line 5 is a
       type of special method called a
       `constructor <https://en.wikipedia.org/wiki/Constructor_(object-oriented_programming)>`_. It is
       *automatically* called whenever a new instance is created. This special method is often used to
       set initial values for any `instance attributes <https://en.wikipedia.org/wiki/Instance_variable>`_.

    #. The ``self`` keyword denotes that an attribute is unique for each *instance* of a class, or operates on
       attributes that are unique for each instance of a class.

    Classes are an invaluable tool for developers and we've only covered the basics here. There are `many,
    many more class mechanics and nuances <https://docs.python.org/3/tutorial/classes.html>`_
    that are outside the scope of this tutorial.


.. _data_sources:

- **(1) Data Sources**

  A :mod:`data source <src.system.data_sources.data_source>` is a definition that provides access to external
  model data. For example:

  - Model points, contained in a *\*.csv* file.
  - Model assumptions, contained in a *\*.json* file.
  - Market data, contained in a Snowflake database.

  It provides this functionality in two ways:

  .. _data_source_cache:

  .. graphviz::

     digraph {
        node [fontname="Arial"];
        rankdir="LR";

        ExternalData [label="External Data" shape="folder"];
        Cache [shape="cylinder"];
        my_access_cache_method [shape="none" fontname="consolas"];
        my_other_access_cache_method [shape="none" fontname="consolas"];

        ExternalData -> Cache;
        Cache -> my_access_cache_method;
        Cache -> my_other_access_cache_method;
     }

  #. When the model runs, data for each data source is loaded into an internal
     `cache <https://en.wikipedia.org/wiki/Cache_(computing)>`_.
  #. The model developer defines
     `methods <https://en.wikipedia.org/wiki/Method_(computer_programming)>`_ to access data from
     the cache. This allows other objects in the :ref:`object model <object_model>` to access the cache
     without having to navigate the internal structure of the cache.

  .. _data_sources_root:

  Passing multiple data sources throughout the model is cumbersome, so the model developer
  aggregates individual data sources into a single
  :class:`data sources root <src.system.data_sources.DataSourcesRoot>` object, which is then passed
  around the model:

  .. graphviz::

     digraph {
        node [fontname="Arial"];
        rankdir="LR";

        DataSourcesRoot [shape="folder"];
        DataSource1 [shape="cylinder"];
        DataSource2 [shape="cylinder"];
        DataSource3 [shape="cylinder"];

        DataSource1 -> DataSourcesRoot;
        DataSource2 -> DataSourcesRoot;
        DataSource3 -> DataSourcesRoot;
     }

  Data sources can also be `nested <https://en.wikipedia.org/wiki/Nesting_(computing)>`_ using
  :class:`namespaces <src.system.data_sources.namespace.DataSourceNamespace>` and
  :class:`collections <src.system.data_sources.collection.DataSourceCollection>` .
  That is, data sources can contain other data sources. For example:

  - A model point data source might contain data sources for individual people and contracts.
  - A market data data source might contain data sources that point to external feeds, like
    `Bloomberg <https://www.bloomberg.com/professional/product/market-data/>`_ or
    `Treasury.gov <https://home.treasury.gov/treasury-daily-interest-rate-xml-feed>`_.

  Data sources are typically used:

  #. To set initial values for :ref:`projection values <projection_values>` within
     :ref:`projection entities <projection_entities>`.
  #. To provide data for :ref:`projection entities <projection_entities>` while a
     :ref:`projection <projections>` is running.

.. _projection_entities:

- **(2) Projection Entities**

  A :class:`projection entity <src.system.projection_entity.ProjectionEntity>`
  is anything that can be projected forwards in time. For example:

  - An insurance contract.
  - A person.

  .. _projection_values:

  Projection entities contain **(3) projection values**.
  :class:`Projection values <src.system.projection_entity.projection_value.ProjectionValue>`
  track and store the future states of a projection entity. For example:

  - An insurance contract might have:
     - A premium payment.
     - A cash surrender value.

  - A person might have:
     - An attained age.
     - A marital status.

  Projection entities also define `methods <https://en.wikipedia.org/wiki/Method_(computer_programming)>`_
  that operate on projection values. For example:

  - An insurance contract might define:
     - A *premium payment* method, which adds a premium payment to the contract.
     - A *surrender* method, which triggers a surrender calculation and benefit release.

  - A person might define:
     - A *death* method, which triggers a death benefit calculation and benefit release
       on a life insurance product.
     - A *marriage* method, which alters the marital status.

  Projection entities can also be `nested <https://en.wikipedia.org/wiki/Nesting_(computing)>`_.
  That is, projection entities can contain other projection entities. For example:

  - An insurance contract might have:
     - Riders.
     - Sub-accounts.

  - A person might have:
     - A cat.

.. _projections:

- **(4) Projections**

  A :class:`projection <src.system.projection.Projection>` is composed of
  :ref:`projection entities <projection_entities>`. For example,
  a life insurance projection might consist of:

  - A life insurance contract.
  - A covered person.
  - An economic index that drives the life insurance contract's account value growth.

  A projection connects projection entities together, defining a logical sequence of
  projection entity `method <https://en.wikipedia.org/wiki/Method_(computer_programming)>`_ calls
  within a *single* time period.

  The projection will then execute the sequence over and over again across a
  specified number of time periods, calculating and updating :ref:`projection values <projection_values>`
  as it goes along.

  Once the projection completes, it will print all projection values.
