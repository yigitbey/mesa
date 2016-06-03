``mesa.time`` --- Time and agent scheduling in Mesa
============================================================

.. automodule:: mesa.time

Overview
-----------------

Time in most models advances in discrete **steps**. In each step, some
(generally all) of the agents will be activated in sequence and take action.
Then the next step begins.

There are often three different methods all named ``step`` which define the
levels of activation. At the highest level is the ``step`` method of a Model
class: this advances the entire model by one step, and includes the agent
activations, and (if relevant) any model-level updates, and data collection.
This step method is implemented in the specific model class.

Within the model ``step`` method


Basic Schedulers
-----------------