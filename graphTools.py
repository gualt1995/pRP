import networkx as nx


def graph_loader(filename):
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
    return G


def kruskal(graph):
    return nx.minimum_spanning_tree(graph)


def build_graph_of_solution(solution, graph):
    G = nx.Graph(graph)
    for i in range(0, len(solution)):
        if solution[i] == '0':
            G.remove_node(str(i+1))
    return G


def size_of_solution(graph):
    nb_nodes = len(graph)
    nodes_list = list(graph.nodes.data('term'))
    cpt = 0
    for node in nodes_list:
        if node[1]:
            cpt += 1
    return nb_nodes - cpt


def fitness_evaluation(solution, graph):
    m = 50
    sub_graph = build_graph_of_solution(solution, graph)
    kurskal_sub = kruskal(sub_graph)
    res = 0
    for edge in nx.get_edge_attributes(kurskal_sub, "weight").values():
        res += edge
    if nx.is_connected(kurskal_sub):
        return res
    else:
        nb_nodes = len(kurskal_sub)
        nb_edges = kurskal_sub.number_of_edges()
        return res + m * ((nb_nodes - 1) - nb_edges)


# graph = graphloader("B/b01.stp")
#print(graph.nodes.data())
#for e in graph.edges.data():
#    print(e)
#print(graph.number_of_nodes())
#nx.draw(graph)
#plt.show()
