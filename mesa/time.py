'''
Mesa Time Module
=================================

Objects for handling the time component of a model. In particular, this module
contains Schedulers, which handle agent activation. A Scheduler is an object
which controls when agents are called upon to act, and when.

The activation order can have a serious impact on model behavior, so it's
important to specify it explicity. Example simple activation regimes include
activating all agents in the same order every step, shuffling the activation
order every time, activating each agent *on average* once per step, and more.

Key concepts:
    Step: Many models advance in 'steps'. A step may involve the activation of
    all agents, or a random (or selected) subset of them. Each agent in turn
    may have their own step() method.

    Time: Some models may simulate a continuous 'clock' instead of discrete
    steps. However, by default, the Time is equal to the number of steps the
    model has taken.


TODO: Have the schedulers use the model's randomizer, to keep random number
seeds consistent and allow for replication.

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
