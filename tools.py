import networkx as nx
import matplotlib.pylab as plt
import random


def full_generation(nb_gen, size, proba):
    """Generate a new population based on a given probability.

    Args:
        nb_gen (int): Number of solutions to generate.
        size (int): Size of the solutions
        proba (float | tuple): Probability for a vertex to be taken
            in the solution (i.e. being set to 1). If the probability is
            a tuple, a random p between proba[0] and proba[1] will be chosen.

    Returns: (list string)
        List of solutions
    """
    res = list()
    for i in range(nb_gen):
        p = random.uniform(proba[0], proba[1]) if type(proba) != float else proba
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


def draw_graph(G):
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
    # nx.draw_networkx_edge_labels(G, pos=pos)
    plt.show()