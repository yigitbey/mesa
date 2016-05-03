from mesa import Agent


class VirusAgent(Agent):
    '''
        Virus on a Network agent
    '''
    def __init__(self, pos, agent_type):

        #self.unique_id = pos
        #self.pos = pos
        #self.type = agent_type

        self.infected = False
        self.resistant = False

    def step(self, model):
        pass
