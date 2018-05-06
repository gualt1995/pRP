import networkx as nx


def graph_loader(filename):
    """Load a graph from an stp file."""
    G = nx.Graph()
    file = open(filename, "r")
    lines = file.readlines()
    build = False
    term = False
    for line in lines:
        if not build:
            if line == "SECTION Graph\n":
                build = True
            elif line == "SECTION Terminals\n":
                term = True
        else:
            words = line.split()
            if words[0] == "E":
                G.add_edge(words[1], words[2], weight=int(words[3]))
            elif words[0] == "END":
                build = False
        if term:
            words = line.split()
            if words[0] == "T":
                G.nodes[words[1]]['term'] = True
            elif words[0] == "END":
                term = False

    G.graph['non_term_nodes'] = [node_label for node_label in G
                                 if not G.nodes[node_label].get("term", False)]
    G.graph['term_nodes'] = [node_label for node_label in G
                                 if G.nodes[node_label].get("term", False)]

    return G


def kruskal(graph):
    """Return minimum spanning tree of the given `graph`."""
    return nx.minimum_spanning_tree(graph)


def build_graph_of_solution(solution, graph):
    """Given a solution and graph, return the sub graph inferred from
    the solution.

    Args:
        solution (string)
        graph (networkx.Graph)

    Returns: (networkx.Graph)
        Sub graph induced from the solution.
    """
    solution_nodes = [graph.graph['non_term_nodes'][i] for i in range(len(solution)) if solution[i] == '1']
    return graph.subgraph(solution_nodes + graph.graph['term_nodes'])


def size_of_solution(graph):
    """Return the necessary size of a solution for a given graph.

    Args:
        graph (networkx.Graph): Graph to evaluate.

    Returns: (int)
        Number of non terminal nodes.
    """
    return len(graph.graph['non_term_nodes'])


def fitness_evaluation(solution, graph):
    """Return the fitness of a solution, that is the total weight of the
    solution. If a solution is non-admissible, a penalty is applied.

    Args:
        solution (string): Solution to evaluate.
        graph (networkx.Graph): Corresponding graph.

    Returns: (int)
        Fitness value of the solution.
    """
    M = 500
    sub_graph = build_graph_of_solution(solution, graph)
    kruskal_sub = kruskal(sub_graph)
    res = kruskal_sub.size('weight')
    graph.edges
    # TODO: Change .size; inefficient ?
    # for edge in nx.get_edge_attributes(kruskal_sub, "weight").values():
    #     res += edge
    if kruskal_sub.number_of_edges() != kruskal_sub.number_of_nodes()-1:
        nb_nodes = kruskal_sub.number_of_nodes()
        nb_edges = kruskal_sub.number_of_edges()
        res += M * ((nb_nodes - 1) - nb_edges)

    print(".", end="", flush=True)
    return res