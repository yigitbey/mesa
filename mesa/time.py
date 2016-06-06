"""``mesa.time`` contains classes for handling time in models. In particular,
it contains Schedluer classes, which control the agent activation regime --
which agents are called upon to act, and when. Example simple activation
regimes include activating all agents in the same order every step, shuffling
the activation order every time, activating each agent *on average* once per
step, and more.

The activation order can have a serious impact on model behavior. Using these
Scheduler clases allows modelers to easily and explicitly specify the
activation regime being used. By maintaining a (more or less) consistent API,
we make it easy to quickly swap one activation regime for another, in order
to test whether this changes the model's overall behavior.

Scheduler API
^^^^^^^^^^^^^^

A Scheduler is generally created inside the model's init function::

    from mesa import Model, Agent
    from mesa.time import BaseScheduler
    
    class MyModel(Model):
        def __init__(self):
            self.schedule = BaseScheduler(self)

Agents are added to the schedule using the ``add`` method::
    
        # ...
            a = MyAgent(unique_id)
            self.schedule.add(a)


And can be removed using ``remove``, e.g.::

    def kill_agent(self, agent):
        '''Remove an agent from the model.'''
        self.schedule.remove(agent)


To run all the agents according to the Scheduler's specified regime, use the
``step`` method, e.g.::

    def step(self):
        self.schedule.step()

``add`` and ``remove`` are implemented in  ``BaseScheduler``, and can be
inherited directly. `

`step`` is what differentiates each Scheduler, since that is where the actual
activation logic is specified. For simple schedulers (e.g. ``BaseScheduler``)
the agent activation is contained in each agent's ``step`` method. 


"""

import random


class BaseScheduler(object):
    """Simple scheduler; activates agents in the order they were added.

    Assumes that each agent added has a *step* method, which accepts a model
    object as its single argument.

    (This is explicitly meant to replicate the scheduler in MASON).
    """

    model = None
    steps = 0
    time = 0
    agents = []

    def __init__(self, model):
        '''Create a new, empty BaseScheduler.

        Parameters
        -----------
            model : mesa.Model
                The model which contains the scheduler. 
        '''

        self.model = model
        self.steps = 0
        self.time = 0
        self.agents = []

    def add(self, agent):
        '''Add an Agent object to the schedule.

        Parameters
        -----------
            agent : mesa.Agent
                An Agent to be added to the schedule. 
                Must have a ``step`` method
        '''
        self.agents.append(agent)

    def remove(self, agent):
        '''Remove all instances of a given agent from the schedule.

        Parameters
        -----------
            agent : mesa.Agent
                An agent previously added to the schedule, to be removed.
        '''
        while agent in self.agents:
            self.agents.remove(agent)

    def step(self):
        '''Execute the step of all the agents, one at a time.'''
        
        for agent in self.agents:
            agent.step(self.model)
        self.steps += 1
        self.time += 1

    def get_agent_count(self):
        '''
        Returns the current number of agents in the queue.
        '''

        return len(self.agents)


class RandomActivation(BaseScheduler):
    '''
    A scheduler which activates each agent once per step, in random order,
    with the order reshuffled every step.

    This is equivalent to the NetLogo 'ask agents...' and is generally the
    default behavior for an ABM.

    Assumes that all agents have a step(model) method.
    '''

    def step(self):
        '''
        Executes the step of all agents, one at a time, in random order.
        '''
        random.shuffle(self.agents)

        for agent in self.agents:
            agent.step(self.model)
        self.steps += 1
        self.time += 1


class SimultaneousActivation(BaseScheduler):
    '''
    A scheduler to simulate the simultaneous activation of all the agents.

    This scheduler requires that each agent have two methods: step and advance.
    step(model) activates the agent and stages any necessary changes, but does
    not apply them yet. advance(model) then applies the changes.
    '''
    def step(self):
        '''
        Step all agents, then advance them.
        '''
        for agent in self.agents:
            agent.step(self.model)
        for agent in self.agents:
            agent.advance(self.model)
        self.steps += 1
        self.time += 1


class StagedActivation(BaseScheduler):
    '''
    A scheduler which allows agent activation to be divided into several stages
    instead of a single `step` method. All agents execute one stage before
    moving on to the next.

    Agents must have all the stage methods implemented. Stage methods take a
    model object as their only argument.

    This schedule tracks steps and time separately. Time advances in fractional
    increments of 1 / (# of stages), meaning that 1 step = 1 unit of time.
    '''

    stage_list = []
    shuffle = False
    shuffle_between_stages = False
    stage_time = 1

    def __init__(self, model, stage_list=["step"], shuffle=False,
            shuffle_between_stages=False):
        '''
        Create an empty Staged Activation schedule.

        Args:
            model: Model object associated with the schedule.
            stage_list: List of strings of names of stages to run, in the
                         order to run them in.
            shuffle: If True, shuffle the order of agents each step.
            shuffle_between_stages: If True, shuffle the agents after each
                                    stage; otherwise, only shuffle at the start
                                    of each step.
        '''
        super().__init__(model)
        self.stage_list = stage_list
        self.shuffle = shuffle
        self.shuffle_between_stages = shuffle_between_stages
        self.stage_time = 1 / len(self.stage_list)

    def step(self):
        '''
        Executes all the stages of all agents.
        '''

        if self.shuffle:
            random.shuffle(self.agents)
        for stage in self.stage_list:
            for agent in self.agents:
                getattr(agent, stage)(self.model)  # Run stage
            if self.shuffle_between_stages:
                random.shuffle(self.agents)
            self.time += self.stage_time

        self.steps += 1
