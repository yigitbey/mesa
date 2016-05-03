import networkx as nx
from random import choice

from mesa import Agent, Model


class VirusAgent(Agent):

    def __init__(self, infected, resistant):

        self.infected = False
        self.resistant = False


class VirusModel(Model):

    def __init__(self, N, G=nx.Graph(), avg_node_degree=6):
        self.num_agents = N
        self.graph = G

        for i in range(self.num_agents):
            # create nodes
            a = VirusAgent(i)
            G.add_node(a)

        # create edges
        # setting average node degree to '6' <-- TODO turn to slider

        num_links = (avg_node_degree * self.num_agents / 2)
        while len(G.edges()) <= num_links:
            first_node = choice(G.nodes())
            possible_nodes = G.nodes()
            possible_nodes.remove(first_node)
            second_node = choice(possible_nodes)

            # If there is no edge create an edge.
            # ^^ Turn this into a function that finds two nodes that are unlinked



