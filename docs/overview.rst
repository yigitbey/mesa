
Overview of Mesa
================

Mesa is a Python framework for developing, analyzing and visualizing agent-based models. Unlike some other ABM tools (such as `NetLogo <https://ccl.northwestern.edu/netlogo/>`_ and `Repast Simphony <http://repast.sourceforge.net/>`_), Mesa isn't a stand-alone development environment. Instead, it provides a library of pre-written Python code for common ABM components and tools, which developers can use to construct, analyze and visualize their models. These tools are meant to be used together, but don't have to be. And since Mesa is just Python (and some JavaScript for the interactive visualization), any of these components can be extended, modified, and combined with other Python libraries and tools.

Features
--------
Mesa provides

- components for developing agent-based models, including multiple schedulers and types of space;

- tools for analyzing these models, such as data collectors and batch runners;

- a system for implementing browser-based interactive model visualizations;

- full compatibility with the rest of the scientific Python ecosystem.

Who is Mesa for?
----------------

Mesa is for anybody interested in using Python for agent-based modeling across different fields, from the social sciences to biology to mathematics. For now, it assumes a beginner to intermediate level of programming knowledge (you should know what classes are, for example).

Mesa is still a new framework under active development. We don't regularly make changes to it that break backwards compatibility, but we can't yet promise that we won't.

Overview of Modules
---------------------

Mesa is modular, meaning that it provides a variety of classes which work well together but can also be used separately. There are roughly three overall categories:

1. **Modeling:** These are classes used to build the models themselves: core Model and Agent classes; schedulers to handle agent activation; and spatial classes to handle agent locations.
2. **Analysis:** These are classes which help extract useful data from models: a DataCollector to collect data from each model run, and a BatchRunner for running a model many times and analyzing how its outputs change with different inputs.
3. **Visualization:** These classes let you interactively visualize your model run in a web browser. They include a different visualization modules (putting agents on a grid, or tracking the value of some variable over time), and a ModularServer which creates the browser-based interface.

A complete Mesa model uses classes from all three categories. The figure below provides a representation of how such a model is architectured. There's the model itself, which consists of agents, with locations in a space and activated by a scheduler. Data on the model and agents is recorded by the data collector. Model data is pulled into the server, which sends it to the browser, which renders it via JavaScript.

.. image:: images/mesa_diagram.png
   :width: 75%
   :scale: 100%
   :alt: Diagram of Mesa objects.
   :align: center


Modeling modules
~~~~~~~~~~~~~~

To build a model, you need the following:

* **Model class** to store the model-level parameters and serve as a container for the rest of the components. This is usually a subclass of the core `mesa.Model` class.

* **Agent class(es)** which describe the model agent behaviors. These are usually subclasses of `Mesa.Agent` and implement a `step(model)` method.

* **Scheduler** which controls the agent activation regime (what order agents act in), and handles time in the model in general. There are several types of schedulers provided, which can be used without being subclassed. For details, see :doc:`the time module <time>`

* **space** components describing the space the agents are situated in (if any). These can also be used without being subclassed.


Analysis modules
~~~~~~~~~~~~~~~~

Not every model *needs* these modules, but they provide useful tools for getting data out of your model runs to study more systematically.

* **Data collectors** are used to record data from each model run.
* **Batch runners** automate multiple runs and parameter sweeps -- running the model with different parameters, to see how they change its behavior.


Visualization modules
~~~~~~~~~~~~~~~~~~~~~

A visualization lets you directly observe model runs, seeing the dynamics that emerge from it and making sure that it's behaving in the way you want it to. Mesa handles visualizations in a browser window, using JavaScript. It provides a set of pre-built components, which can be instantiated for a particular model in Python and automatically generate the corresponding objects in the browser window. It's also easy to write your own components with some basic JavaScript knowledge.

Some visualization modules we'll use here include:

* **Grid** visualization,
* **Chart** display module,
* The **ModularServer** itself.

What next?
^^^^^^^^^^

- :doc:`Complete Mesa Tutorial <intro-tutorial>`