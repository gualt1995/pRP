from tools import *
from operator import itemgetter
from operators import operators
from selections import selections
import graph_tools as gt


def genetic_algorithm(G, max_steps=100, pop_size=100, operator='single_point_crossover',
                      selection_process='sus', p_operator=1, p_gen=(0.2, 0.5),
                      construction_heuristic='shortest_path', generation_type='heuristic',
                      mutation_type='uniform_mutation', elitism=True, elitism_propotion=0.1):
    """Tries to resolve the minimum Steiner tree problem with a genetic algorithm.

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
        construction_heuristic (string): Type of heuristic used for the population generation
        p_operator (float): Probability for the operator to have an effect on the
            selected parents.

    Returns: (float)
        Approximation of the optimal solution
    """
    population = generation_types[generation_type](pop_size, G, p_gen=p_gen, heuristic=construction_heuristic)
    selection_process_cls = selections[selection_process]
    operator_func = operators[operator]
    mutation_func = operators[mutation_type]

    print("==== SteinerTree Genetic Algorithm ====")
    print("Population size : {}, Max steps : {}".format(pop_size, max_steps))
    print("Crossover operator : {}".format(operator))
    print("Selection process : {}".format(selection_process))
    print("Generation type : {}".format(generation_type))
    if generation_type == 'heuristic': print("Heuristic of construction : {}".format(construction_heuristic))
    print("Mutation type : {}".format(mutation_type))
    print("Elitism : {}".format(elitism))

    population_fitness = [(population[i], 1/gt.fitness_evaluation(population[i], G)) for i in range(pop_size)]
    sorted_pop_fitness = None

    print("Generated {} starting candidate solutions, actual={}".format(len(population), len(set(population))))

    elites_proportion = int(pop_size*elitism_propotion)
    non_elites_proportion = int(pop_size*(1-elitism_propotion))

    for _ in range(max_steps):
        new_pop_fitness = list()

        sorted_pop_fitness = sorted(population_fitness, key=itemgetter(1), reverse=True)
        selection_pcss = selection_process_cls(solutions=sorted_pop_fitness)

        for _i in range(int(pop_size/2)):
            parents = selection_pcss.select(k=2)
            child1, child2 = operator_func(parents[0], parents[1], p_operator)
            child1_m = mutation_func(child1)
            child2_m = mutation_func(child2)
            new_pop_fitness.append((child1_m, 1/gt.fitness_evaluation(child1_m, G)))
            new_pop_fitness.append((child2_m, 1/gt.fitness_evaluation(child2_m, G)))

        if elitism:
            sorted_all_pop = sorted(population_fitness + new_pop_fitness,
                                    key=itemgetter(1), reverse=True)
            new_pop_fitness = sorted_all_pop[:elites_proportion] \
                              + random.sample(sorted_all_pop[elites_proportion:], non_elites_proportion)

        population_fitness = new_pop_fitness
        print("Cost={}, iter={}, pop_size={}, actual={}, Highest cost={}".format(1/sorted_pop_fitness[0][1], _,
                                                                                 len(population_fitness),
                                                                len(set([p[0] for p in population_fitness])),
                                                                1 / sorted_pop_fitness[-1][1]))

    print()
    return sorted_pop_fitness[0]


if __name__ == "__main__":
    graph = gt.graph_loader("D/d07.stp")
    solution = genetic_algorithm(graph)
    solution_graph = gt.kruskal(gt.build_graph_of_solution(solution[0], graph))
    print("Solution cost = {}".format(gt.fitness_evaluation(solution[0], graph)))
    draw_graph(solution_graph)