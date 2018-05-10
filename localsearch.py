from tools import *
from heuristics import *


def generation(G, construction_heuristic='shortest_path', generation_type='heuristic', p_gen=(0.2, 0.5)):
    """Tries to resolve the minimum Steiner tree problem with Local search algorithm.

    Args:
        G (networkx.Graph): Graph of the problem.
        construction_heuristic (string): Type of heuristic used for the population generation
        generation_type (string): Type of generation.
        p_gen (float or tuple, optional): Proportion of bits to 1; used for the generation
            of the initial population.

    Returns: (float)
        Approximation of the optimal solution
    """

    print("==== SteinerTree Local search Algorithm ====")
    print("Generation type : {}".format(generation_type))
    if generation_type == 'heuristic': print("Heuristic of construction : {}".format(construction_heuristic))

    gen = generation_types[generation_type](1, G, p_gen=p_gen, heuristic=construction_heuristic)
    prevsol = gen[0]
    solgraph = gt.build_graph_of_solution(prevsol, G)
    print("starting fitness : " + str(gt.fitness_evaluation(prevsol, G)))
    newsol = neighbour(G, solgraph, prevsol)
    while prevsol != newsol:
        print("new local search iteration")
        prevsol = newsol
        newsol = neighbour(G, solgraph, prevsol)
    return gt.fitness_evaluation(newsol, G)


def neighbour(G, gsol, solution):
    """A local search algorithm that finds the first solution of the problem(if any) that has
    a better fitness score than the one its given.

    Args:
        G (networkx.Graph): Graph of the problem.
        gsol (networkx.Graph): Graph of current solution of the problem.
        solution (string): solution of the problem stored in string format.

    Returns: (float)
        a new solution of the problem with a better fitness score than the previous one
    """
    prevfitness = gt.fitness_evaluation(solution,G)
    for i in range(len(solution)):
        node = G.graph['non_term_nodes'][i]
        if solution[i] == "0":
            neighbours = G.neighbors(node)
            cpt = 0
            for node in neighbours:
                if node in gsol.nodes():
                    cpt += 1
            if cpt > 1:
                newsol = list(solution)
                newsol[i] = "1"
                newsol = "".join(newsol)
                fitness = gt.fitness_evaluation(newsol, G)
                if fitness < prevfitness:
                    return newsol
        else:
            newsol = list(solution)
            newsol[i] = "0"
            newsol = "".join(newsol)
            fitness = gt.fitness_evaluation(newsol, G)
            if fitness < prevfitness:
                return newsol
    return solution


graph = gt.graph_loader("C/c07.stp")
print("result fitness : " + str(generation(graph)))
