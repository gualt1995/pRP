from tools import *
import graph_tools as gt
import random

def write_csv(test_name, data):
    with open('report/results/{}.csv'.format(test_name), 'w') as f:
        for d in data:
            s = ",".join(map(str, d)) + "\n"
            f.write(s)


def test_random_generation():
    data = [['inst', 'prop', 'cost']]

    for instance in ('B/b02.stp', 'B/b08.stp', 'C/c18.stp'):
        G = gt.graph_loader(instance)
        size = gt.size_of_solution(G)
        sols = list()
        for _ in range(3):
            p = random.uniform(0.2, 0.5)
            sols.append((p, generation(size, p)))
        for solution in sols:
            data.append([instance[2:5], "{:.2f}".format(solution[0]), "{:.0f}".format(gt.fitness_evaluation(solution[1], G))])

    write_csv(test_random_generation.__name__, data)


def test_heuristic(type):
    data = [['inst', 'cost']]

    for instance in ('B/b02.stp', 'B/b08.stp', 'C/c18.stp'):
        G = gt.graph_loader(instance)
        sols = heuristic_generation(3, G, heuristic=type)
        for solution in sols:
            data.append([instance[2:5], "{:.0f}".format(gt.fitness_evaluation(solution, G))])

    write_csv(test_heuristic.__name__, data)


if __name__ == "__main__":
    test_heuristic('mst')