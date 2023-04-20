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

Let's take what we've learned so far and see how that can be used to build our annuity model.

Data Sources
^^^^^^^^^^^^

#. **The Data Sources Root**

   In the previous tutorial, we mentioned that we define a single :ref:`DataSourcesRoot <data_sources_root>` object
   that holds all other data sources. We've done that for the annuity model here with
   :class:`~src.data_sources.annuity.AnnuityDataSources`:

   .. code-block:: python
        :linenos:
        :lineno-start: 26
        :emphasize-lines: 2

        class AnnuityDataSources(
            DataSourcesRoot
        ):

   Note that :class:`~src.data_sources.annuity.AnnuityDataSources` inherits from
   :class:`~src.system.data_sources.DataSourcesRoot`:

   .. inheritance-diagram:: src.data_sources.annuity.AnnuityDataSources
      :parts: 1

#. **Annuity Data Sources Attributes**

   By itself, a :class:`~src.system.data_sources.DataSourcesRoot` object doesn't contain anything and isn't
   particularly useful. To make it useful, we have to connect it to external data. There are three types
   of objects that help us manage this:

   #. A :mod:`~src.system.data_sources.data_source` object, which is a Pythonic representation of external data. This
      is how data is connected to our model. Supported data formats are listed in this
      :mod:`module <src.system.data_sources.data_source>`.
   #. A :class:`~src.system.data_sources.namespace.DataSourceNamespace` object, which holds:

      #. :mod:`~src.system.data_sources.data_source` objects.
      #. Other :class:`~src.system.data_sources.namespace.DataSourceNamespace` objects.
      #. :class:`~src.system.data_sources.collection.DataSourceCollection` objects.

      These objects are declared **before** the model starts running, ahead of runtime.

      .. note::
        You might have noticed in the inheritance diagram above that :class:`~src.system.data_sources.DataSourcesRoot`
        inherits from :class:`~src.system.data_sources.namespace.DataSourceNamespace`.
        This is because :class:`~src.system.data_sources.DataSourcesRoot` is a *special case* of
        :class:`~src.system.data_sources.namespace.DataSourceNamespace`.

   #. A :class:`~src.system.data_sources.collection.DataSourceCollection`, which behaves very similarly to a
      :class:`~src.system.data_sources.namespace.DataSourceNamespace`, except child objects are created on-the-fly
      **while** the model is running (during runtime), and are not known ahead of time.

   To add one of these objects, we declare it as an attribute in
   :class:`~src.data_sources.annuity.AnnuityDataSources`. For example, including this code in the
   :meth:`constructor <src.data_sources.annuity.AnnuityDataSources.__init__>` adds a
   :class:`~src.data_sources.annuity.model_points.ModelPoints` object to our
   :class:`~src.data_sources.annuity.AnnuityDataSources` object:

   .. code-block:: python
        :linenos:
        :lineno-start: 76

        # Model points
        self.model_points = ModelPoints(
            path=join(
                self.path,
                'model_points.json'
            )
        )

#. **The Model Point File**

   We can take a closer look at the :class:`~src.data_sources.annuity.model_points.ModelPoints` object to see exactly
   how data is loaded into the model. From the class definition:

   .. code-block:: python
        :linenos:
        :lineno-start: 10
        :emphasize-lines: 2

        class ModelPoints(
            ModelPointsBase
        ):

   We see that :class:`~src.data_sources.annuity.model_points.ModelPoints` inherits from
   :class:`~src.data_sources.model_points.ModelPointsBase`:

   .. inheritance-diagram:: src.data_sources.annuity.model_points.ModelPoints
      :parts: 1

   And further up the inheritance diagram, we see that :class:`~src.data_sources.model_points.ModelPointsBase` inherits
   from both :class:`~src.system.data_sources.collection.DataSourceCollection` *and*
   :class:`~src.system.data_sources.data_source.file_json.DataSourceJsonFile`.

   From this, we can conclude that :class:`~src.data_sources.annuity.model_points.ModelPoints`:

   #. Reads data from a JSON file.
   #. Maintains a collection of child objects, determined at runtime.

   In our model point file, our child objects are :class:`~src.data_sources.annuity.model_points.model_point.ModelPoint`
   classes. We know this by examining the constructor methods. For
   :class:`~src.data_sources.annuity.model_points.ModelPoints`:

   .. code-block:: python
        :linenos:
        :lineno-start: 35
        :emphasize-lines: 4

        ModelPointsBase.__init__(
            self=self,
            path=path,
            model_point_type=ModelPoint
        )

   The constructor calls the constructor for :class:`~src.data_sources.model_points.ModelPointsBase`,
   passing in :class:`~src.data_sources.annuity.model_points.model_point.ModelPoint` as the ``model_point_type``
   parameter.

   In the constructor for :class:`~src.data_sources.model_points.ModelPointsBase`:

   .. code-block:: python
        :linenos:
        :lineno-start: 49
        :emphasize-lines: 3, 4, 5

        for data in [row[1] for row in self.cache.iterrows()]:

            instance = model_point_type(
                data=data
            )

            self[instance.id] = instance

   We see that we're constructing and storing new instances of ``model_point_type`` by looping through the
   :ref:`cache <data_source_cache>`. In this case, (since we've inherited from
   :class:`~src.system.data_sources.data_source.file_json.DataSourceJsonFile`), the cache contains elements from
   the JSON file and we're passing those into the
   :class:`~src.data_sources.annuity.model_points.model_point.ModelPoint` constructor.

#. **A Model Point**

   Now let's take a look at a :class:`~src.data_sources.annuity.model_points.model_point.ModelPoint` within the
   model point file:

   .. inheritance-diagram:: src.data_sources.annuity.model_points.model_point.ModelPoint
      :parts: 1

   From the inheritance diagram, we see that :class:`~src.data_sources.annuity.model_points.model_point.ModelPoint`
   inherits from :class:`src.data_sources.model_points.model_point.ModelPointBase`.

   Inside :class:`src.data_sources.model_points.model_point.ModelPointBase`, we see an
   :attr:`src.data_sources.model_points.model_point.ModelPointBase.id` property:

   .. code-block:: python
        :linenos:
        :lineno-start: 36
        :emphasize-lines: 14

            @property
            def id(
                self
            ) -> str:

                """
                Unique identifier for this model point. This could be a Policy Number, integer,
                `GUID <https://en.wikipedia.org/wiki/Universally_unique_identifier>`_,
                or any other unique code.

                :return: Model point ID.
                """

                return self.cache[DEFAULT_COL]['id']

   Note that this property returns a value from the cache. **This is how data makes its way into the model.** When the
   data source is initialized, it loads raw data into a cache. Then the model developer defines an attribute
   that returns data from the cache.

   .. note::
        Why so complicated? Why not read data directly from the file and just use a raw data feed in the model? We
        do this because:

        #. **Write once, use everywhere**. Once we've written this logic, we can use it everywhere in the model with
           zero duplicate code.

        #. **Abstraction**. Other model developers do not need to know the details. They can take
           a data source for granted and just use it. This also lends itself to parallel development, where
           one model developer implements data sources while another implements model logic.

#. **Zooming Out**

   Now we've seen the end-to-end process for one unit of data, here's the model input package in its entirety:

   .. graphviz::

    digraph {
        edge [dir="back"];
        node [fontname="Arial"];
        rankdir="LR";

        AnnuityDataSources [shape="box3d"];

        EconomicScenarios [shape="folder"];
        EconomicScenario [shape="cylinder"];
        get_rate [shape="ellipse"];

        ModelPoints [shape="folder"];
        ModelPoint [shape="cylinder"];
        id_mp [label="id" shape="ellipse"];
        product_type [shape="ellipse"];
        product_name [shape="ellipse"];
        issue_date [shape="ellipse"];
        Annuitants [shape="folder"];
        Annuitant [shape="cylinder"]
        id_annuitant [label="id" shape="ellipse"];
        gender [shape="ellipse"];
        date_of_birth [shape="ellipse"];
        Riders [shape="folder"];
        Gmwb [shape="folder"];
        rider_type [shape="ellipse"];
        rider_name [shape="ellipse"];
        benefit_base [shape="ellipse"];
        first_withdrawal_date [shape="ellipse"];
        Gmdb [shape="folder"];
        Accounts [shape="folder"];
        Account [shape="cylinder"];
        id_account [label="id" shape="ellipse"];
        account_type [shape="ellipse"];
        account_name [shape="ellipse"];
        account_value [shape="ellipse"];
        account_date [shape="ellipse"];
        Premiums [shape="folder"];
        Premium [shape="cylinder"];
        premium_date [shape="ellipse"];
        premium_amount [shape="ellipse"];

        Mortality [shape="folder"];
        BaseMortality [shape="cylinder"];
        base_mortality_rate [shape="ellipse"];
        MortalityImprovement [shape="cylinder"];
        mortality_improvement_rate [shape="ellipse"];
        MortalityImprovementDates [shape="cylinder"];
        mortality_improvement_start_date [shape="ellipse"];
        mortality_improvement_end_date [shape="ellipse"];

        PolicyholderBehaviors [shape="folder"];
        BaseLapse [shape="cylinder"];
        base_lapse_rate [shape="ellipse"];
        ShockLapse [shape="cylinder"];
        shock_lapse_multiplier [shape="ellipse"];
        Annuitization [shape="cylinder"];
        annuitization_rate [shape="ellipse"];

        Product [shape="folder"];
        BaseProduct [shape="folder"];
        SurrenderCharge [shape="cylinder"];
        surrender_charge_rate [shape="cylinder"];
        cdsc_period [shape="cylinder"];
        CreditingRate [shape="folder"];
        FixedCreditingRate [shape="cylinder"];
        crediting_rate [shape="ellipse"];
        IndexedCreditingRate [shape="cylinder"];
        index [shape="ellipse"];
        term [shape="ellipse"];
        cap [shape="ellipse"];
        spread [shape="ellipse"];
        participation_rate [shape="ellipse"];
        floor [shape="ellipse"];
        GmdbRider [shape="folder"];
        GmdbCharge [shape="cylinder"];
        charge_rate_gmdb [label="charge_rate" shape="ellipse"];
        GmdbTypes [shape="cylinder"];
        gmdb_type [shape="ellipse"];
        GmwbRider [shape="folder"];
        GmwbBenefit [shape="cylinder"];
        av_active_withdrawal_rate [shape="ellipse"];
        av_exhaust_withdrawal_rate [shape="ellipse"];
        GmwbCharge [shape="cylinder"];
        charge_rate_gmwb [label="charge_rate" shape="ellipse"];

        AnnuityDataSources -> EconomicScenarios;
        EconomicScenarios -> EconomicScenario;
        EconomicScenario -> get_rate;

        AnnuityDataSources -> ModelPoints;
        ModelPoints -> ModelPoint;
        ModelPoint -> id_mp;
        ModelPoint -> product_type;
        ModelPoint -> product_name;
        ModelPoint -> issue_date;
        ModelPoint -> Annuitants;
        Annuitants -> Annuitant;
        Annuitant -> id_annuitant;
        Annuitant -> gender;
        Annuitant -> date_of_birth;
        ModelPoint -> Riders;
        Riders -> Gmwb;
        Gmwb -> rider_type;
        Gmwb -> rider_name;
        Gmwb -> benefit_base;
        Gmwb -> first_withdrawal_date;
        Riders -> Gmdb;
        Gmdb -> rider_type;
        Gmdb -> rider_name;
        ModelPoint -> Accounts;
        Accounts -> Account;
        Account -> id_account;
        Account -> account_type;
        Account -> account_name;
        Account -> account_value;
        Account -> account_date;
        Account -> Premiums;
        Premiums -> Premium;
        Premium -> premium_date;
        Premium -> premium_amount;

        AnnuityDataSources -> Mortality;
        Mortality -> BaseMortality;
        BaseMortality -> base_mortality_rate;
        Mortality -> MortalityImprovement;
        MortalityImprovement -> mortality_improvement_rate;
        Mortality -> MortalityImprovementDates;
        MortalityImprovementDates -> mortality_improvement_start_date;
        MortalityImprovementDates -> mortality_improvement_end_date;


        AnnuityDataSources -> PolicyholderBehaviors;
        PolicyholderBehaviors -> BaseLapse;
        BaseLapse -> base_lapse_rate;
        PolicyholderBehaviors -> ShockLapse;
        ShockLapse -> shock_lapse_multiplier;
        PolicyholderBehaviors -> Annuitization;
        Annuitization -> annuitization_rate;

        AnnuityDataSources -> Product;

        Product -> BaseProduct;
        BaseProduct -> SurrenderCharge;
        SurrenderCharge -> surrender_charge_rate;
        SurrenderCharge -> cdsc_period;
        BaseProduct -> CreditingRate;
        CreditingRate -> FixedCreditingRate;
        FixedCreditingRate -> crediting_rate;
        CreditingRate -> IndexedCreditingRate;
        IndexedCreditingRate -> index;
        IndexedCreditingRate -> term;
        IndexedCreditingRate -> cap;
        IndexedCreditingRate -> spread;
        IndexedCreditingRate -> participation_rate;
        IndexedCreditingRate -> floor;

        Product -> GmdbRider;
        GmdbRider -> GmdbCharge;
        GmdbCharge-> charge_rate_gmdb;
        GmdbRider -> GmdbTypes;
        GmdbTypes -> gmdb_type;

        Product -> GmwbRider;
        GmwbRider -> GmwbBenefit;
        GmwbBenefit -> av_active_withdrawal_rate;
        GmwbBenefit -> av_exhaust_withdrawal_rate;
        GmwbRider -> GmwbCharge;
        GmwbCharge -> charge_rate_gmwb;
    }

Projection Entities
^^^^^^^^^^^^^^^^^^^



Projection
^^^^^^^^^^


