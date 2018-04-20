import networkx as nx
import matplotlib.pylab as plt
import random
import graphTools as gt
import operator


def fullgeneration(nbgen, size, proba):
    res = list()
    for i in range(0,nbgen):
        res.append(generation(size, proba))
    return res


def generation(size,proba):
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
def selection(popratingsorted):
    res1 = res2 = ""
    p1 = random.random()
    p2 = random.random()
    for j in popratingsorted:
        if j[1] < p1:
            res1 = j
            break
    for j in popratingsorted:
        if j[1] < p2:
            res2 = j
            break
    return res1, res2


def croissement(parent1,parent2,pcroissement):
    #TODO on coupe a la moitee pas sure que c'est bien ca
    point = int(len(parent1))
    length = len(parent1)-1
    p1 = random.random()
    if pcroissement < p1:
        firstpar1, secondpar1 = parent1[0][:int(len(parent1[0]) / 2)], parent1[0][int(len(parent1[0]) / 2):]
        firstpar2, secondpar2 = parent2[0][:int(len(parent2[0]) / 2)], parent2[0][int(len(parent2[0]) / 2):]
        parent1 = (firstpar1+secondpar2, parent1[1])
        parent2 = (firstpar2+secondpar1, parent2[1])
    return parent1, parent2





def genetic_algorithm(graph,steps,popsize,pstart,pselect,pcroissement):
    sollen = gt.sizeofsolution(graph)
    pop = fullgeneration(popsize, sollen, pstart)
    poprating = dict()
    for k in range(0, steps):
        newpop = list()
        for i in range(0, popsize):
            poprating[pop[i]] = gt.fitnessevaluation(pop[i], graph)
        popratingsorted = sorted(poprating.items(), key=operator.itemgetter(1))
        popproba = list()
        for i in range(0,len(popratingsorted)):
            popproba.append((popratingsorted[i][0],pselect*pow((1-pselect), i)))
        for i in range(0, int(popsize/2)):
            # version ou on ajoute que les fils a la solution;
            parent1, parent2 = selection(popproba)
            fils1, fils2 = croissement(parent1, parent2, pcroissement)
            fils1m = (mutation(fils1[0]), fils1[1])
            fils2m = (mutation(fils2[0]), fils2[1])
            newpop.append(fils1m[0])
            newpop.append(fils2m[0])
        pop = newpop;
        print(newpop[0])
    for i in range(0, popsize):
        poprating[pop[i]] = gt.fitnessevaluation(pop[i], graph)
    popratingsorted = sorted(poprating.items(), key=operator.itemgetter(1))
    return popratingsorted[-1]


graph = gt.graphloader("B/b01.stp")
print(genetic_algorithm(graph, 50, 10, 0.2, 0.8, 0.1))
