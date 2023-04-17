.. _tutorial_pt1:

Tutorial, Part 1
================

Introduction
------------

**Welcome to the modeling framework tutorial!** This tutorial assumes the audience:

- Has **no** prior Python knowledge or experience, but some basic programming experience in another
  language (like `Visual Basic for Applications (VBA)
  <https://en.wikipedia.org/wiki/Visual_Basic_for_Applications>`_).
- Has *some* actuarial modeling knowledge.
- Runs a **Windows 10** desktop environment.
- Has **administrator privileges** on their device, and can install and configure software.

This tutorial is split into 3 parts:

#. A brief, practical introduction to setting up a working environment and generating a set of model results.
#. A conceptual overview of the modeling framework.
#. A deeper dive into how the modeling framework is used to create a sample annuity model.

.. note::
    The modeling framework relies on Object-Oriented Programming (*OOP*) concepts and mechanics.
    We'll introduce these as we go.

Installation and Setup
----------------------

This modeling framework was developed using (and works best with) PyCharm Community Edition.

#. **Download and Install Python**

   #. Download Python 3.11.X from here:

      `<https://www.python.org/ftp/python/3.11.3/python-3.11.3-amd64.exe>`_

   #. Install Python by double-clicking on the executable:

      .. image:: images/install_python.png

      #. Check *Use admin privileges when install py.exe*.
      #. Check *Add python.exe to PATH*.
      #. Click *Install Now* when ready.

   #. Once the installer completes, click *Disable path length limit*:

      .. image:: images/install_python_path_length_limit.png

#. **Download and Install PyCharm Community Edition**

   #. Download PyCharm Community Edition from here:

      `<https://www.jetbrains.com/pycharm/download/download-thanks.html?platform=windows&code=PCC>`_

   #. Install PyCharm by double-clicking on the executable:

      `<https://www.jetbrains.com/help/pycharm/installation-guide.html#standalone>`_

      Under the **Installation Options**, select *Add "Open Folder as Project"*

      .. image:: images/install_pycharm_options.png

#. **Download and Unzip the Project from GitHub**

   #. Download the project from here:

      `<https://github.com/chingdaotze/actuarial-model/archive/refs/heads/main.zip>`_

   #. Unzip the project by right-clicking and selecting *Extract All...*:

      .. image:: images/python_project_extract.png

#. **Open the Project in PyCharm**

   #. Navigate to the extraction location and right-click.
      Then click *Open Folder as PyCharm Community Edition Project*:

      .. image:: images/python_project_open.png

   #. If prompted, select *Trust Project*:

      .. image:: images/trust_project.png

   .. _virtual_environment:

#. **Set up a Virtual Environment**

   #. Go to *File > Settings...*

      .. image:: images/pycharm_settings.png

   #. Navigate to `Project: \* > Python Interpreter > Add Interpreter`:

      .. image:: images/pycharm_add_interpreter.png

      And click on *Add Local Interpreter*.

      .. image:: images/pycharm_add_interpreter_confirm.png

      The click *OK*.

   #. Click *OK* again to save your changes in the *Settings* dialog.

      .. image:: images/pycharm_ok.png

   .. _required_packages:

#. **Install the Required Packages**

   #. Click on Terminal to open up a terminal session:

   #. In the terminal session, type:

      .. code-block:: powershell

            pip install -r "install\requirements.txt"

      .. image:: images/install_reqs.png

      Then hit ``ENTER`` to execute the command.

   #. Once the command completes, you can close out the terminal session:

      .. image:: images/close_terminal.png

Running the Model
-----------------

To run the model:

#. In the upper right-hand corner, ensure that the run configuration is set to *main*.
   Then click the "Play" button to run the model:

   .. image:: images/run_model_1.png

#. The model should start running and console output should appear in PyCharm's *Run* window:

   .. image:: images/run_model_2.png

   .. note::

     .. _log_file:

     Console output is :mod:`also piped to a log file as plain text <src.system.logger>`. The
     location of the log file can be found in the console output:

     .. image:: images/run_model_3.png

   .. _model_output:

#. Model output can be found in the modeling framework's *output* directory:

   .. image:: images/run_model_4.png

   For the sample annuity model, the *output* directory is organized like so:

   .. code-block:: text

       \ Model point ID
           \ Economic scenario number
               Model output *.csv files
