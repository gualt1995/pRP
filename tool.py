import networkx as nx
import matplotlib.pylab as plt
import random


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


def generation(size,proba):
    res = ""
    for bit in range(size):
        if random.randint(1,101) < proba:
            res += "1"
        else:
            res += "0"
    return res

print(mutation("00001111"))