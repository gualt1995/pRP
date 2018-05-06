from itertools import combinations
import networkx as nx
import graph_tools as gt


def _distance_graph(G):
    """Build the complete distance graph of the terminal nodes of G. For each
    pair of terminal nodes, an edge represents the shortest path in G.

    Args:
         G (networkx.Graph): Original graph

    Returns:
        Distance graph of the terminal nodes.
    """
    terminal_pairs = combinations(G.graph['term_nodes'], 2)
    dist_graph = nx.Graph()

    for pair in terminal_pairs:
        path = nx.shortest_path(G, pair[0], pair[1], weight='weight')
        dist_graph.add_edge(pair[0], pair[1], weight=len(path), path=path)

    return dist_graph


def _replace_distance_by_path(G, original_graph):
    """From a distance graph and the original graph, replaces the edges
    by the corresponding shortest paths of the original graph.

    Args:
        G: Distance graph.
        original_graph: Original graph.

    Returns: (networkx.Graph)
    """
    new_graph = nx.Graph()

    for edge in G.edges.data('path'):
        path = edge[2]
        for i in range(len(path)-1):
            new_graph.add_edge(path[i], path[i+1], weight=original_graph.edges[path[i], path[i+1]]['weight'])

    for node_label in new_graph.nodes:
        new_graph.nodes[node_label]['term'] = original_graph.nodes[node_label].get('term', False)

    return new_graph


def _prune_graph(G):
    """Removes any non-terminal nodes with a degree of 1 from the graph.
    A new graph is returned.

    Args:
        G: Graph to prune.

    Returns: (networkx.Graph * boolean)
        The pruned graph and a boolean indicating if the graph was actually
        modified.
    """
    new_graph = nx.Graph(G)

    number_of_modification = 0
    prunable_nodes = [node for node in G.nodes if G.degree[node] == 1 and not G.nodes[node].get('term', False)]
    while len(prunable_nodes) > 0:
        new_graph.remove_nodes_from(prunable_nodes)
        number_of_modification += 1
        prunable_nodes = [node for node in new_graph.nodes if new_graph.degree[node] == 1
                          and not new_graph.nodes[node].get('term', False)]

    return new_graph, number_of_modification > 0


def h_shortest_path(G):
    """Shortest path construction heuristic for the Steiner Tree problem. The graph is
    constructed like so:
    - G1 = distance graph of the terminal nodes.
    - G2 = minimum spanning tree of G1.
    - G3 = G2 with every edge replaced by the shortest path in G.
    - G4 = minimum spanning tree of G3.
    - G5 = pruned G4.

    Args:
        G: Original graph.

    Returns: (networkx.Graph)
    """
    G1 = _distance_graph(G)
    G2 = gt.kruskal(G1)
    G3 = _replace_distance_by_path(G2, G)
    G4 = gt.kruskal(G3)
    G5, _ = _prune_graph(G4)
    return G5


def h_mst(G):
    """Minimum spanning tree construction heuristic for the Steiner Tree problem.
    The graph returned is a minimum spanning tree pruned to its maximum without
    removing any terminal nodes.

    Args:
        G: Original graph.

    Returns: (networkx.Graph)
    """
    graph_modified = True
    new_graph = G

    while graph_modified:
        new_graph = gt.kruskal(new_graph)
        new_graph, graph_modified = _prune_graph(new_graph)

    return new_graph


construction_heuristics = {
    'shortest_path': h_shortest_path,
    'mst': h_mst
}
