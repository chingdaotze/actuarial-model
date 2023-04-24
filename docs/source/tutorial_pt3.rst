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

.. _data_sources_annuity_model:

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
   particularly useful. To make it useful, we have to add external data connections. There are three types
   of objects that help us manage this:

   #. A :mod:`~src.system.data_sources.data_source` object, which is a Pythonic representation of external data. This
      is how data is connected to our model. Supported data formats are listed in this
      :mod:`module <src.system.data_sources.data_source>`.
   #. A :class:`~src.system.data_sources.namespace.DataSourceNamespace` object, which holds:

      #. :mod:`~src.system.data_sources.data_source` objects.
      #. Other :class:`~src.system.data_sources.namespace.DataSourceNamespace` objects.
      #. :class:`~src.system.data_sources.collection.DataSourceCollection` objects.

      These objects are declared as instance attributes **before** the model starts running, ahead of runtime.

      .. note::
        You might have noticed in the inheritance diagram above that :class:`~src.system.data_sources.DataSourcesRoot`
        inherits from :class:`~src.system.data_sources.namespace.DataSourceNamespace`.
        This is because :class:`~src.system.data_sources.DataSourcesRoot` is a *special case* of
        :class:`~src.system.data_sources.namespace.DataSourceNamespace`.

   #. A :class:`~src.system.data_sources.collection.DataSourceCollection`, which behaves very similarly to a
      :class:`~src.system.data_sources.namespace.DataSourceNamespace`, except child objects are created on-the-fly
      **while** the model is running (during runtime), and are not known ahead of time.

   To add one of these objects to our :class:`~src.data_sources.annuity.AnnuityDataSources` object,
   we declare it as an attribute. For example, including this code in the
   :meth:`constructor <src.data_sources.annuity.AnnuityDataSources.__init__>` adds a
   :class:`~src.data_sources.annuity.model_points.ModelPoints` object named ``model_points`` to our
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

   Then in the constructor for :class:`~src.data_sources.model_points.ModelPointsBase`:

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
   inherits from :class:`~src.data_sources.model_points.model_point.ModelPointBase`.

   Inside :class:`~src.data_sources.model_points.model_point.ModelPointBase`, we see an
   :attr:`~src.data_sources.model_points.model_point.ModelPointBase.id` property:

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
   that reads the cache and returns data.

   .. note::
        Why so complicated? Why not read data directly from the file and just use raw data in the model? We
        do this because:

        #. **Write once, use everywhere**. Once we've written this logic, we can use it everywhere in the model with
           zero duplicate code.

        #. **Abstraction**. Other model developers do not need to know:

           #. How the cache is loaded (From a CSV file? A database? An XML file from a REST API?).
           #. How the cache is structured (What columns represent what data? What do the row indexes mean?).

           They can simply take a data source for granted and just use it. This also lends itself to
           parallel development, where one model developer can implement data sources while another
           implements model logic.

#. **Zooming Out**

   Now we've seen the end-to-end process for one unit of data (in pink), here's the model inputs package in its entirety:

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
        id_mp [label="id" shape="ellipse" fillcolor="darksalmon" style="filled"];
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

.. note::
  **To-Do's**

  - There may be a way to combine :class:`~src.system.data_sources.namespace.DataSourceNamespace` and
    :class:`~src.system.data_sources.collection.DataSourceCollection` into a single class that
    supports *both* static and dynamic child objects.
  - Currently, the modeling framework only supports file-based or Python-based
    :class:`~src.system.data_sources.data_source.base.DataSourceBase` objects, listed in the
    :mod:`~src.system.data_sources.data_source` module. In the future, we can add
    support for more data formats (like databases or data feeds), leveraging the Python community's
    vast libraries of open-source code.

.. _projection_entities_annuity_model:

Projection Entities
^^^^^^^^^^^^^^^^^^^

#. **Model Overview**

   .. graphviz::

    digraph {
        edge [dir="back"];
        node [fontname="Arial", shape="Box"];

        Riders [shape="tab"];
        Accounts [shape="tab"];
        Premiums [shape="tab"];
        Annuitants [shape="tab"];

        "Economy";

        "Base Contract" -> Annuitants;
        Annuitants -> "Annuitant";

        "Base Contract" -> Riders;
        Riders -> "GMWB";
        Riders -> "GMDB MAV";
        Riders -> "GMDB RAV";
        Riders -> "GMDB ROP";

        "Base Contract" -> Accounts;
        Accounts -> Fixed -> Premiums;
        Accounts -> Indexed -> Premiums;
        Accounts -> Separate -> Premiums;
        Premiums -> Premium;
    }

   The annuity model consists of two top-level :class:`~src.system.projection_entity.ProjectionEntity` objects:

   - :class:`~src.projection_entities.economy.Economy` - the economic environment for this projection.

   - :class:`~src.projection_entities.products.annuity.base_contract.BaseContract` - the annuity contract in this
     projection.

   The :class:`~src.projection_entities.products.annuity.base_contract.BaseContract`
   contains several nested
   :class:`~src.system.projection_entity.ProjectionEntity` objects:

   - :class:`~src.projection_entities.people.annuitants.Annuitants` - the annuitant(s) in this projection.

     - :class:`~src.projection_entities.people.annuitants.annuitant.Annuitant` - a single annuitant in this projection.

   - A `list <https://docs.python.org/3/tutorial/datastructures.html#more-on-lists>`_ of elected riders:

     - :class:`~src.projection_entities.products.annuity.riders.gmwb.Gmwb` - Guaranteed Minimum Withdrawal Benefit
       (GMWB) rider.
     - :class:`~src.projection_entities.products.annuity.riders.gmdb.mav.GmdbMav` - Guaranteed Minimum Death Benefit
       (GMDB) rider, with ratchet option.
     - :class:`~src.projection_entities.products.annuity.riders.gmdb.rav.GmdbRav` -
       GMDB rider, with return of account value option.
     - :class:`~src.projection_entities.products.annuity.riders.gmdb.rop.GmdbRop` -
       GMDB rider, with return of premium option.

     .. note::
        Riders are optional. It is possible to have a
        :class:`~src.projection_entities.products.annuity.base_contract.BaseContract` with *no* riders.

   - A `list <https://docs.python.org/3/tutorial/datastructures.html#more-on-lists>`_ of accounts:

     - :class:`~src.projection_entities.products.annuity.base_contract.account.fa.FixedAccount` - Fixed interest
       crediting account. Typically used for Fixed Annuity contracts, but available for all contracts.
     - :class:`~src.projection_entities.products.annuity.base_contract.account.ia.IndexedAccount` - Indexed
       strategy crediting account, typically used for Fixed Indexed Annuity contracts.
     - :class:`~src.projection_entities.products.annuity.base_contract.account.va.SeparateAccount` - Separate
       crediting account, typically used for Variable Annuity contracts.

     Each account also maintains a `list <https://docs.python.org/3/tutorial/datastructures.html#more-on-lists>`_
     of :class:`~src.projection_entities.products.annuity.base_contract.account.premium.Premium` 's.

     .. note::
        - A policy must have *at least* one account.
        - It is possible for a policy to have multiple accounts of the same type. For example,
          a policy could have two Fixed accounts that credit interest at different rates.

#. **Fixed Account Deep Dive**

   #. *Navigating to the Account Class*

      To see how a :class:`~src.system.projection_entity.ProjectionEntity` works, let's take a look at the
      :class:`~src.projection_entities.products.annuity.base_contract.account.fa.FixedAccount`:

      .. code-block:: python
        :linenos:
        :lineno-start: 14
        :emphasize-lines: 2

        class FixedAccount(
            Account
        ):

      From the inheritance diagram:

      .. inheritance-diagram:: src.projection_entities.products.annuity.base_contract.account.fa.FixedAccount
         :parts: 1

      We see that a :class:`~src.projection_entities.products.annuity.base_contract.account.fa.FixedAccount` inherits
      from an :class:`~src.projection_entities.products.annuity.base_contract.account.Account`.

   #. *Account Super Classes*

      Let's take a close look at the :class:`~src.projection_entities.products.annuity.base_contract.account.Account`
      object. Starting with the class definition:

      .. code-block:: python
        :linenos:
        :lineno-start: 14
        :emphasize-lines: 2, 3

        class Account(
            ProjectionEntity,
            ABC
        ):

      There are two super classes:

      .. inheritance-diagram:: src.projection_entities.products.annuity.base_contract.account.Account
         :parts: 1

      - Line 15 states that an :class:`~src.projection_entities.products.annuity.base_contract.account.Account`
        inherits from :class:`~src.system.projection_entity.ProjectionEntity`, so an ``Account`` is a
        type of ``ProjectionEntity``.
      - Line 16 states that an :class:`~src.projection_entities.products.annuity.base_contract.account.Account`
        *also* inherits from `ABC <https://docs.python.org/3/library/abc.html#abc.ABC>`_, which means that this
        class is an
        `ABstract Class <https://en.wikipedia.org/wiki/Abstract_type>`_. Abstract classes *cannot* be used
        to create instances, and are typically used to represent an *abstract* object (in this case, an *abstract*
        account). Since this class is an abstract class, it can only be used through inheritance.

   #. *Premium Tracking Within an Account*

      Moving down into the :ref:`constructor <constructor_note>`, we declare a
      :attr:`list of premiums <src.projection_entities.products.annuity.base_contract.account.Account.premiums>`:

      .. code-block:: python
        :linenos:
        :lineno-start: 69

        self.premiums = self._get_new_premiums(
            t1=self.init_t
        )

      Where ``_get_new_premiums`` returns a list of premiums paid at
      :attr:`~src.system.projection_entity.ProjectionEntity.init_t`. This attribute stores all premiums
      that are (and will be) paid into the account,
      and will grow as this projection entity is projected into the future.

   #. *Declaring Projection Values*

      Further down the constructor, we declare :class:`~src.system.projection_entity.projection_value.ProjectionValue`
      objects. For example:

      .. code-block:: python
        :linenos:
        :lineno-start: 80

        self.premium_cumulative = ProjectionValue(
            init_t=self.init_t,
            init_value=self._calc_total_premium()
        )

        self.interest_credited = ProjectionValue(
            init_t=self.init_t,
            init_value=0.0
        )

      These two attributes (along with other :class:`~src.system.projection_entity.projection_value.ProjectionValue`
      objects) represent *key values* that we're interested in tracking. In the code above:

      #. :attr:`~src.projection_entities.products.annuity.base_contract.account.Account.premium_cumulative` tracks
         the cumulative premiums paid into the ``Account``. Its initial value is provided by the
         ``_calc_total_premium`` method, and is set at time
         :attr:`~src.system.projection_entity.ProjectionEntity.init_t`.
      #. :attr:`~src.projection_entities.products.annuity.base_contract.account.Account.interest_credited` tracks
         the point-in-time interest paid into the ``Account``. Its initial value is set to ``0.0`` at time
         :attr:`~src.system.projection_entity.ProjectionEntity.init_t`.

   #. *Declaring Methods*

      :class:`~src.system.projection_entity.ProjectionEntity` objects typically declare methods that calculate
      and update :class:`~src.system.projection_entity.projection_value.ProjectionValue` objects.

      For example:

      .. code-block:: python
        :linenos:
        :lineno-start: 80

        def process_withdrawal(
            self,
            withdrawal_amount: float
        ) -> None:

            """
            Reduces :attr:`account value <account_value>` by a withdrawal amount
            and records the :attr:`withdrawal amount <withdrawal>`.

            .. warning:
                This algorithm does not check if the withdrawal amount is greater than the account value.

            :param withdrawal_amount: Withdrawal amount.
            :return: Nothing.
            """

            self.withdrawal[self.time_steps.t] = withdrawal_amount
            self.account_value[self.time_steps.t] = self.account_value - self.withdrawal

      This method:

      #. Sets the :attr:`withdrawal_amount <src.projection_entities.products.annuity.base_contract.account.Account.withdrawal>`
         :class:`~src.system.projection_entity.projection_value.ProjectionValue` at time
         :attr:`t <src.system.projection.time_steps.TimeSteps.t>`.

         .. note::
                The withdrawal amount is calculated somewhere outside the method and passed in as a method
                `argument <https://en.wikipedia.org/wiki/Parameter_(computer_programming)>`_.

      #. Sets the :attr:`withdrawal_amount <src.projection_entities.products.annuity.base_contract.account.Account.account_value>`
         :class:`~src.system.projection_entity.projection_value.ProjectionValue` at time
         :attr:`t <src.system.projection.time_steps.TimeSteps.t>`, by subtracting two
         :class:`~src.system.projection_entity.projection_value.ProjectionValue` 's with each other.

   #. *Overriding Methods*

      In the previous section we've seen how to declare a method that interacts with class attributes.
      The :class:`~src.projection_entities.products.annuity.base_contract.account.Account` class also contains a
      :meth:`~src.projection_entities.products.annuity.base_contract.account.Account.credit_interest`
      **abstract method**:

      .. code-block:: python
        :linenos:
        :lineno-start: 219

            @abstractmethod
            def credit_interest(
                self
            ) -> None:

                """
                Abstract method that represents an interest crediting mechanism. Inherit and override to implement
                a custom crediting algorithm (e.g. RILA, separate account crediting, or indexed crediting).

                :return: Nothing.
                """

                ...

      An abstract method declares that a method *should* exist, and what arguments the method should take,
      but doesn't provide an *implementation* for the method. Note:

      #. There is an `abstractmethod <https://docs.python.org/3/library/abc.html#abc.abstractmethod>`_ decorator over
         method name.
      #. The function body is empty and only contains
         `ellipsis <https://docs.python.org/3/library/constants.html#Ellipsis>`_.

      You can think of an abstract method as a "placeholder" within an abstract class, where the implementation
      is provided by a derived class.

      In this case, recall that the :class:`~src.projection_entities.products.annuity.base_contract.account.Account`
      class is an `abstract class <https://en.wikipedia.org/wiki/Abstract_type>`_, and is inherited by
      :class:`~src.projection_entities.products.annuity.base_contract.account.fa.FixedAccount`:

      .. inheritance-diagram:: src.projection_entities.products.annuity.base_contract.account.fa.FixedAccount
         :parts: 1

      If we go back up to :class:`~src.projection_entities.products.annuity.base_contract.account.fa.FixedAccount`, we
      see :class:`~src.projection_entities.products.annuity.base_contract.account.fa.FixedAccount` 's implementation
      of the :meth:`~src.projection_entities.products.annuity.base_contract.account.fa.FixedAccount.credit_interest`:

      .. code-block:: python
        :linenos:
        :lineno-start: 36

            def credit_interest(
                self
            ) -> None:

                r"""
                Credits interest to the sub\-account, where the fixed crediting rate is from
                :meth:`~src.data_sources.annuity.product.base.crediting_rate.fixed.FixedCreditingRate.crediting_rate`.

                .. math::
                    interest \, credited = account \, value \times crediting \, rate \times years \, elapsed

                :math:`years \, elapsed` is calculated using :func:`~src.system.date.calc_partial_years`.

                :return: Nothing
                """

                crediting_rate = self.data_sources.product.base_product.crediting_rate.fixed.crediting_rate(
                    account_name=self.account_data_source.account_name
                )

                partial_years = calc_partial_years(
                    dt1=self.time_steps.t,
                    dt2=self.time_steps.prev_t
                )

                crediting_rate *= partial_years

                self.interest_credited[self.time_steps.t] = self.account_value * crediting_rate

                self.account_value[self.time_steps.t] = self.account_value + self.interest_credited

.. note::
        **Why do we do this?**

        There is *a lot* of common logic between the various account types. For example, each account
        processes premiums and takes withdrawals in the exact same way. This allows us to put all the
        common account logic in one "generic" account, then inherit and override to create "specialized"
        types of accounts.

        We can use this generalize / specialize mechanism for many objects within an actuarial model,
        and programming in general.

.. note::
  **To-Do's**

  - The underlying model output storage format is a
    `Pandas Dataframe <https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html>`_ and the model generates
    its output \*.csv files using the
    `DataFrame.to_csv <https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_csv.html>`_ method. However,
    there are *many* more output formats that can be implemented by leveraging the power of DataFrames,
    including:

    - `Excel files <https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_excel.html>`_
    - `Graphs and charts <https://pandas.pydata.org/pandas-docs/version/0.13.1/visualization.html>`_
    - `Other data formats, like parquet
       <https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_parquet.html>`_

Projection
^^^^^^^^^^

#. **The Annuity Economic Liability Projection**

   We've defined :ref:`inputs for our projection <data_sources_annuity_model>`
   and we've defined :ref:`objects for our projection <projection_entities_annuity_model>`. The last
   thing to do is link everything together in a :class:`~src.system.projection.Projection`.

   To see how that works, let's take a look at the
   :class:`~src.projections.annuity.base.economic_liability.EconomicLiabilityProjection` class. Starting from the top:

   .. code-block:: python
      :linenos:
      :lineno-start: 16
      :emphasize-lines: 2

        class EconomicLiabilityProjection(
            Projection
        ):

   We can see :class:`~src.projections.annuity.base.economic_liability.EconomicLiabilityProjection` is a type of
   :class:`~src.system.projection.Projection`, since it inherits from :class:`~src.system.projection.Projection`:

   .. inheritance-diagram:: src.projection_entities.products.annuity.base_contract.account.fa.FixedAccount
      :parts: 1

   Moving down into the :ref:`constructor <constructor_note>`, we declare our
   :ref:`top-level <projection_entities_annuity_model>`
   :class:`~src.system.projection_entity.ProjectionEntity` objects:

   .. code-block:: python
      :linenos:
      :lineno-start: 41

        self.economy = Economy(
            time_steps=self.time_steps,
            data_sources=self.data_sources
        )

        self.base_contract = BaseContract(
            time_steps=self.time_steps,
            data_sources=self.data_sources
        )

#. **Defining the Order of Operations**

   Now that our :class:`~src.system.projection_entity.ProjectionEntity` objects have been declared in our
   projection, we can define our projection's order of operations (within a time step) by overriding the
   :meth:`src.system.projection.Projection.project_time_step` method. Here's the
   :meth:`overriden method <src.projections.annuity.base.economic_liability.EconomicLiabilityProjection.project_time_step>`:

   .. code-block:: python
      :linenos:
      :lineno-start: 99

            def project_time_step(
                self
            ) -> None:

                """
                Annuity Economic Liability Projection transaction order and method calls within a single time step.

                :return: Nothing.
                """

                self.economy.age_economy()

                self.base_contract.age_contract()

                self.base_contract.process_premiums()

                self.base_contract.credit_interest()

                self.base_contract.assess_charges()

                self.base_contract.process_withdrawals()

                self.base_contract.update_gmdb_naar()

                self.base_contract.update_cash_surrender_value()

                self.base_contract.annuitants.update_decrements()

   The :meth:`~src.projections.annuity.base.economic_liability.EconomicLiabilityProjection.project_time_step` method
   calls other methods within the top-level projection entities. This defines the order of operations within a single
   time step.

What's Next?
------------

These tutorials aim to provide a high-level understanding of the modeling framework, but don't cover every
detail or bit of functionality. For a complete reference, please consult the
:ref:`Model Documentation <model_documentation>` for documentation on the annuity sample model, or
:ref:`System Documentation <system_documentation>` for documentation on the modeling framework.

Thanks for reading!

.. image:: images/dfa.png
    :width: 600
