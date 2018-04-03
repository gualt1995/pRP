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
                G.add_edge(words[1], words[2], weight=words[3])
            elif words[0] == "END":
                build = False
        if term:
            words = line.split()
            if words[0] == "T":
                G.nodes[words[1]]['term'] = True
            elif words[0] == "END":
                term = False
    return G


def kurskal(graph):
    nx.minimum_spanning_tree(graph)


graph = graphloader("B/b01.stp")
#print(graph.nodes.data())
#for e in graph.edges.data():
#    print(e)
print(test)
#print(graph.number_of_nodes())
#nx.draw(graph)
#plt.show()
