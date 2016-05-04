import networkx as nx
from random import choice

from mesa import Agent, Model


class VirusAgent(Agent):

    def __init__(self, infected=False, resistant=False):

        self.infected = infected
        self.resistant = resistant


class VirusModel(Model):

    # setting average node degree to '6' <-- TODO turn to slider
    def __init__(self, N, G=None, avg_degree=6):
        self.num_agents = N

        self.graph = G
        if not self.graph:
            self.graph = self._create_network(avg_degree)

        print(self.graph)

    # TODO: Discuss - maybe this is abstracted out / generalized?
    def _create_network(self, avg_degree):

        G = nx.Graph()
        for i in range(self.num_agents):
            # create nodes
            a = VirusAgent(i)
            G.add_node(a)

        num_links = (avg_degree * self.num_agents / 2)
        while len(G.edges()) <= num_links:
            first = choice(G.nodes())
            possible_nodes = G.nodes()
            possible_nodes.remove(first)
            second = choice(possible_nodes)

            edges = G.edges()

            # TODO: Rewrite for directed graphs
            # add a way for this to be handled.
            if (first, second) not in edges and (second, first) not in edges:
                G.add_edge(first, second)

        self.graph = G
