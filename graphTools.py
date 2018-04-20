import networkx as nx
import matplotlib.pylab as plt


def graphloader(filename):
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


def buildgraphofsolution(solution, graph):
    G = nx.Graph(graph)
    for i in range(0, len(solution)):
        if solution[i] == '0':
            G.remove_node(str(i+1))
    return G


def sizeofsolution(graph):
    nbnodes = len(graph)
    nodeslist = list(graph.nodes.data('term'))
    cpt = 0
    for node in nodeslist:
        if node[1]:
            cpt += 1
    return nbnodes - cpt

def fitnessevaluation(solution, graph):
    m = 50
    subgraph = buildgraphofsolution(solution, graph)
    kurskalsub = kruskal(subgraph)
    res = 0
    for edge in nx.get_edge_attributes(kurskalsub, "weight").values():
        res += edge
    if nx.is_connected(kurskalsub):
        return res
    else:
        nbnodes = len(kurskalsub)
        nbedges = kurskalsub.number_of_edges()
        return res + m * ((nbnodes - 1) - nbedges)
graph = graphloader("B/b01.stp")
#print(graph.nodes.data())
#for e in graph.edges.data():
#    print(e)
print("test")
#print(graph.number_of_nodes())
#nx.draw(graph)
#plt.show()
