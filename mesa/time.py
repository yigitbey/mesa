'''
This module contains classes for handling the time component of a model. In
particular, it contains Schedulers, which handle agent activation. A Scheduler
is an object which controls when agents are called upon to act, and when.

Time in agent-based models generally advances in discrete steps (sometimes 
called ticks). Within each step of the model, some or all of the model agents
are activated, one at a time. When an agent is activated, it executes whatever
behavior it has been programmed with (e.g. observes its surrounding, moves,
reproduces, dies); then it is another agent's turn to act. There are obviously
variants on this as well. The way agents are activated can have a serious
impact on model behavior, so it's important to specify it explicity. 

There are many possible activation regimes. Here are some examples:
- All agents are activated in the same order every model step.
- All agents are activated every step, in random order.
- Some number *N* random agents are activated every step, in random order.

The schedulers are meant to handle these activation regimes. They have a common
set of methods, so that you can change the activation regime by changing as
little code as possible; ideally only one line. A scheduler object is created
when you instantiate a model; agents are added to the scheduler when they are
created, and removed when they are destroyed. Then the scheduler handles
activating all the agents according to the specified regime.

Note that schedulers are intended to handle only activations of agents and
other objects inside the simulation itself. Often you'll have other things you
want to have happen every step -- for example, collecting data on all the
agents, or writing some output to an external file. These shouldn't go in the
scheduler, but in the model's `step` method.

'''

import random


class BaseScheduler(object):
    '''
    Simplest scheduler; activates agents one at a time, in the order they were
    added.

    Assumes that each agent added has a *step* method, which accepts a model
    object as its single argument.

    (This is explicitly meant to replicate the scheduler in MASON).

    Attributes
    ----------
    model : Model
        The Mesa model object this scheduler is a part of.
    steps : int
        Counter for how many steps the model has run for.
    time : int
        How much simulated time has past; here it is the same as steps.
    agents : list
        List of agents added to the scheduler.
    '''

    model = None
    steps = 0
    time = 0
    agents = []

    def __init__(self, model):
        '''
        Create a new, empty BaseScheduler.

        Parameters
        ----------
        model : Model
            Model this scheduler is associated with.
        '''

        self.model = model
        self.steps = 0
        self.time = 0
        self.agents = []

    def add(self, agent):
        '''
        Add an Agent object to the schedule.

        Parameters
        ----------
        agent : Agent 
            An Agent to be added to the schedule. The agent must have a 
            `step(model)` method.
        '''
        self.agents.append(agent)

    def remove(self, agent):
        '''
        Remove all instances of a given agent from the schedule.

        Parameters
        ----------
        agent : Agent 
            Agent object to remove.
        '''
        while agent in self.agents:
            self.agents.remove(agent)

    def step(self):
        '''
        Runs the `step` method of each agent that has been added to the
        scheduler, in the order the agents were added in.
        '''
        for agent in self.agents:
            agent.step(self.model)
        self.steps += 1
        self.time += 1

    def get_agent_count(self):
        '''
        Returns
        -------
        int
            The number of agents that have been added to the model.
        '''
        return len(self.agents)


class RandomActivation(BaseScheduler):
    '''
    A scheduler which activates each agent once per step, in random order,
    with the order reshuffled every step.

    This is equivalent to the NetLogo 'ask agents...' and is generally the
    default behavior for an ABM.
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

    This scheduler requires that each agent have two methods: `step(model)` and
    `advance(model)`. `step` activates the agent and stages any necessary
    changes, but does not apply them yet. `advance` then applies the changes.
    '''
    def step(self):
        '''
        Step all agents, in fixed order, then advance them.
        '''
        for agent in self.agents:
            agent.step(self.model)
        for agent in self.agents:
            agent.advance(self.model)
        self.steps += 1
        self.time += 1
