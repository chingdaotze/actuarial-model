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

#. Download and Install Python 3.11.X
#. Download and Install PyCharm Community Edition
#. Download and unzip project from GitHub
#. Open project in PyCharm

   .. _virtual_environment:

#. Set up a virtual environment

   .. _required_packages:

#. Install required packages

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
