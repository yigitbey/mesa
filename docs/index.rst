.. Mesa documentation master file, created by
   sphinx-quickstart on Sun Jan  4 23:34:09 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Mesa Documentation
================================

Welcome to Mesa, a Python framework for `agent-based modeling <http://en.wikipedia.org/wiki/Agent-based_model>`_ of social, natural and other `complex systems <http://en.wikipedia.org/wiki/Complex_systems>`_. Mesa is built on several principles, including

* **Modularity:** Mesa doesn't make any assumptions about whether your model will be spatial, or if the agents will be activated in a particular way. Every part of the model needs to be specified, and can be easily subclassed and extended in order to implement custom features.
* **Batteries included:** Mesa is built to meet the needs of researchers and analysts by including tools for collecting data from model runs, performing parameter sweeps, and other key activities. This allows you to build a model, run it many times with different settings, and analyze the results all in the same environment.
* **Separate, in-browser visualization:** Mesa visualizations are kept separate from the models themselves. Like models, visualizations are assembled from standardized modules which are easy to customize, modify or extend. The actual visualization is done in a web browser, avoiding system-specific GUI issues and allowing the use of state-of-the-art JavaScript visualization libraries.


Here are a few places to get started.

If you want a general overview of what Mesa includes, check out the :ref:`overview`.



Contents:

.. toctree::
   :maxdepth: 2

   getting-started
   modindex


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

