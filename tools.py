import networkx as nx
import matplotlib.pylab as plt
import graph_tools as gt
from heuristics import construction_heuristics
import random


def full_generation(nb_gen, G, **kwargs):
    """Generate a new population based on a given probability.

    Args:
        nb_gen (int): Number of solutions to generate.
        size (int): Size of the solutions
        p_gen (float | tuple): Probability for a vertex to be taken
            in the solution (i.e. being set to 1). If the probability is
            a tuple, a random p between proba[0] and proba[1] will be chosen.

    Returns: (list string)
        List of solutions
    """
    size = gt.size_of_solution(G)
    res = list()
    p_gen = kwargs['p_gen']
    for i in range(nb_gen):
        p = random.uniform(p_gen[0], p_gen[1]) if type(p_gen) != float else p_gen
        res.append(generation(size, p))
    return res


def generation(size, proba):
    """Generate a solution based on a given probability.

    Args:
        size (int): Size of the solution
        proba (float): Probability for a vertex to be taken
            in the solution.

    Returns: (string)
        Solution in a string format, (e.g. 0011)
    """
    res = ""
    for bit in range(size):
        if random.randint(1,101) < proba*100:
            res += "1"
        else:
            res += "0"
    print("Generated with p={:.2f} -> {}".format(proba, res))
    return res


def randomise_graph(G, perturbation=(0.05, 1.0)):
    """Randomise the edges' weight of G. Each weight is displaced from their
    original value according to the percentages of `perturbation`.

    Args:
        G: Original graph.
        perturbation (tuple float): Min and max perturbation from the
            original value.

    Returns: (networkx.Graph)
    """
    new_graph = nx.Graph(G)
    for edge in new_graph.edges.data('weight'):
        deviated_value = random.uniform(edge[2] - edge[2]*perturbation[1], edge[2] + edge[2]*perturbation[1])
        new_graph.edges[edge[0], edge[1]]['weight'] = deviated_value

    return new_graph


def heuristic_generation(n, G, **kwargs):
    population = list()
    heuristic = kwargs.get('heuristic', 'shortest_path')

    for _ in range(n):
        G_h = construction_heuristics[heuristic](randomise_graph(G))
        solution = "".join("1" if node in G_h else "0" for node in G.graph['non_term_nodes'])
        population.append(solution)

        print("Generated with h={} -> {}".format(heuristic, solution))

    return population


generation_types = {
    'random': full_generation,
    'heuristic':  heuristic_generation
}


def draw_graph(G, draw_edge_labels=False):
    """Draws a graph.
    Terminal nodes are colored in red.
    Regular nodes are colored in blue.

    Args:
        G (networkx.Graph): Graph to draw.
    """
    pos = nx.spring_layout(G, iterations=30, k=0.5)
    colormap = {
        True: "#af0428",
        False: "#7986CB"
    }
    colors = [colormap[G.nodes[node_label].get('term', False)] for node_label in G]

    nx.draw(G, pos=pos, node_size=50, node_color=colors, edge_color="#BDBDBD")
    # nx.draw_networkx_labels(G, pos=pos)
    if draw_edge_labels:
        nx.draw_networkx_edge_labels(G, pos=pos)
    plt.show()