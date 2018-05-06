from tools import *
from operator import itemgetter
from operators import operators
from selections import selections
import graph_tools as gt


def genetic_algorithm(G, max_steps=100, pop_size=100, operator='single_point_crossover',
                      selection_process='tournament', p_operator=1, p_gen=(0.2, 0.5),
                      construction_heuristic='mst', generation_type='heuristic',
                      mutation_type='uniform_mutation'):
    """Tries to resolve the minimum Steiner tree problem with a genetic algorithm

    Args:
        G (networkx.Graph): Graph of the problem.
        max_steps (int): Maximum number of steps of the algorithm.
        pop_size (int): Population size.
        operator (string): Operator used.
        selection_process (string): Selection process used.
        mutation_type (string): Type of mutation.
        generation_type (string): Type of generation.
        p_gen (float or tuple, optional): Proportion of bits to 1; used for the generation
            of the initial population.
        p_operator (float): Probability for the operator to have an effect on the
            selected parents.

    Returns: (float)
        Approximation of the optimal solution
    """
    population = generation_types[generation_type](pop_size, G, p_gen=p_gen, heuristic=construction_heuristic)
    population_fitness = {population[i]: 1/gt.fitness_evaluation(population[i], G) for i in range(pop_size)}
    sorted_pop_fitness = None
    selection_process_cls = selections[selection_process]
    operator_func = operators[operator]
    mutation_func = operators[mutation_type]

    print("Generated {} random starting candidate solutions".format(len(population)))

    for _ in range(max_steps):
        new_pop_fitness = dict()

        sorted_pop_fitness = sorted(population_fitness.items(), key=itemgetter(1), reverse=True)
        selection_pcss = selection_process_cls(solutions=sorted_pop_fitness)

        for _i in range(int(pop_size/2)):
            # parents = random.choices(sorted_pop_fitness[:int(pop_size*0.1)], k=2)
            parents = selection_pcss.select(k=2)
            # print(parents)
            child1, child2 = operator_func(parents[0], parents[1], p_operator)
            child1_m = mutation_func(child1)
            child2_m = mutation_func(child2)
            l = [(parents[0], population_fitness[parents[0]]),
                              (parents[1], population_fitness[parents[1]]),
                       (child1_m, 1/gt.fitness_evaluation(child1_m, G)),
                       (child2_m, 1/gt.fitness_evaluation(child2_m, G))]
            print([1/e[1] for e in l])
            results = sorted([(parents[0], population_fitness[parents[0]]),
                              (parents[1], population_fitness[parents[1]]),
                       (child1_m, 1/gt.fitness_evaluation(child1_m, G)),
                       (child2_m, 1/gt.fitness_evaluation(child2_m, G))], key=itemgetter(1), reverse=True)

            # Elitism
            new_pop_fitness[results[0][0]] = results[0][1]
            new_pop_fitness[results[1][0]] = results[1][1]

        population_fitness = new_pop_fitness
        print("Cost={}, iter={}".format(1/sorted_pop_fitness[0][1], _))

    print()
    return sorted_pop_fitness[0]


if __name__ == "__main__":
    graph = gt.graph_loader("B/b18.stp")
    solution = genetic_algorithm(graph)
    solution_graph = gt.kruskal(gt.build_graph_of_solution(solution[0], graph))
    print("Solution cost = {}".format(gt.fitness_evaluation(solution[0], graph)))
    draw_graph(solution_graph)