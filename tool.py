import networkx as nx
import matplotlib.pylab as plt
import random
import graphTools as gt
import operator


def full_generation(nb_gen, size, proba):
    res = list()
    for i in range(0, nb_gen):
        res.append(generation(size, proba))
    return res


def generation(size, proba):
    res = ""
    for bit in range(size):
        if random.randint(1,101) < proba*100:
            res += "1"
        else:
            res += "0"
    return res


def mutation(solution):
    res = ""
    for bit in solution:
        if random.randint(1,101) < 5:
            if bit == "0":
                res += "1"
            else:
                res += "0"
        else:
            res += bit
    return res


# returns two selected parents(res1 and res2 are tuples (solution,proba_rating))
def selection(pop_rating_sorted):
    res1 = res2 = ""
    p1 = random.random()
    p2 = random.random()
    for j in pop_rating_sorted:
        if j[1] < p1:
            res1 = j
            break
    for j in pop_rating_sorted:
        if j[1] < p2:
            res2 = j
            break
    return res1, res2


def croisement(parent1, parent2, p_croisement):
    #TODO on coupe a la moitee pas sure que c'est bien ca
    point = int(len(parent1))
    length = len(parent1)-1
    p1 = random.random()
    if p_croisement < p1:
        firstpar1, secondpar1 = parent1[0][:int(len(parent1[0]) / 2)], parent1[0][int(len(parent1[0]) / 2):]
        firstpar2, secondpar2 = parent2[0][:int(len(parent2[0]) / 2)], parent2[0][int(len(parent2[0]) / 2):]
        parent1 = (firstpar1+secondpar2, parent1[1])
        parent2 = (firstpar2+secondpar1, parent2[1])
    return parent1, parent2


def genetic_algorithm(graph, steps, pop_size, p_start, p_select, p_croissement):
    sol_len = gt.size_of_solution(graph)
    pop = full_generation(pop_size, sol_len, p_start)
    pop_rating = dict()
    for k in range(0, steps):
        newpop = list()
        for i in range(0, pop_size):
            pop_rating[pop[i]] = gt.fitness_evaluation(pop[i], graph)
        pop_rating_sorted = sorted(pop_rating.items(), key=operator.itemgetter(1))
        pop_proba = list()
        for i in range(0,len(pop_rating_sorted)):
            pop_proba.append((pop_rating_sorted[i][0], p_select * pow((1 - p_select), i)))
        for i in range(0, int(pop_size / 2)):
            # version ou on ajoute que les fils a la solution;
            parent1, parent2 = selection(pop_proba)
            fils1, fils2 = croisement(parent1, parent2, p_croissement)
            fils1m = (mutation(fils1[0]), fils1[1])
            fils2m = (mutation(fils2[0]), fils2[1])
            newpop.append(fils1m[0])
            newpop.append(fils2m[0])
        pop = newpop
        print(newpop[0])
    for i in range(0, pop_size):
        pop_rating[pop[i]] = gt.fitness_evaluation(pop[i], graph)
    pop_rating_sorted = sorted(pop_rating.items(), key=operator.itemgetter(1))
    return pop_rating_sorted[-1]


def draw_graph(G):
    """

    :param G:
    :return:
    """
    pos = nx.spring_layout(G, iterations=30, k=0.5)
    colormap = {
        True: "#af0428",
        False: "#7986CB"
    }
    colors = [colormap[G.node[node_label].get('term', False)] for node_label in G]

    nx.draw(G, pos=pos, node_size=50, node_color=colors, edge_color="#BDBDBD")
    plt.show()


if __name__ == "__main__":
    graph = gt.graph_loader("B/b01.stp")
    draw_graph(graph)
    print(genetic_algorithm(graph, 50, 10, 0.2, 0.8, 0.1))
