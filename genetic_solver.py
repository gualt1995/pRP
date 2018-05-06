from tools import *
from operator import itemgetter
import graph_tools as gt


def single_point_crossover(parent1, parent2, p_crossover=1.0):
    """Perform a single point crossover on two given parents.
    The point is chosen uniformly and two children are produced.

    Args:
        parent1 (string): First parent.
        parent2 (string): Second parent.
        p_crossover (float): Probability for the operator to have
            an effect on the parents. If no effect, the parents are
            returned.

    Returns: string * string
        The children produced by the operator.
    """
    p = random.random()
    if p_crossover < p:
        index = random.randint(len(parent1))
        firstpar1, secondpar1 = parent1[:index], parent1[index:]
        firstpar2, secondpar2 = parent2[:index], parent2[index:]
        parent1 = firstpar1 + secondpar2
        parent2 = firstpar2 + secondpar1
    return parent1, parent2


def mutation(solution):
    """Generate a solution mutated from a given solution; that is
    for each vertex, the corresponding bit in the solution may be flipped.
    Default mutation probability is 4%.

    Args:
        solution (string): starting solution

    Returns: (string)
        Mutated solution.
    """
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


class Selection:
    """Selection process.

    Attributes:
        _selection_pool (list tuple): All subclasses must compute a
            selection pool from which chromosomes will be selected.
    """

    def select(self, k=2):
        """Select k chromosomes from the selection pool. By default
        the selection pool is assumed to be a list of tuples sorted
        by cumulative fitness.

        Args:
            k (int): Number of chromosomes to select.

        Returns: tuple list
            Chromosomes selected.
        """
        parents = list()
        for _ in range(k):
            parent = None
            p = random.random()
            for candidate in getattr(self, '_selection_pool'):
                if candidate[1] < p:
                    parent = candidate
                else:
                    break
            parents.append(parent)

        return parents


class FitnessProportionateSelection(Selection):
    """Implements a fitness proportionate selection process.
    The selection pool is constructed as a list usable by the
    `Selection.select` function.
    """
    def __init__(self, **kwargs):
        """Construct the selection pool.

        Args:
            solutions (tuple list): List of candidate solutions with
                their associated fitness.
        """
        fitness_sum = sum(s[1] for s in kwargs['solutions'])
        # Build cumulative fitness list..
        self._selection_pool = list()
        cum_sum = 0
        for s in kwargs['solutions']:
            self._selection_pool.append((s[0], cum_sum))
            cum_sum += s[1] / fitness_sum


class TournamentSelection(Selection):
    """Implements a tournament selection. The probability of being chosen
    is highest for the best solution and decreases exponentially for the lower
    ranks.
    """
    DEFAULT_PROBABILITY = 0.5

    def __init__(self, **kwargs):
        """TODO: Multiple tournament for more diversity

        Args:
            solutions (tuple list): List of candidate solutions with
                their associated fitness.
        """
        p = kwargs.get('p', TournamentSelection.DEFAULT_PROBABILITY)
        self._selection_pool = list()
        cum_sum = 0
        for i in range(len(kwargs['solutions'])):
            self._selection_pool.append((kwargs['solutions'][i][0], cum_sum))
            cum_sum += p * pow(1 - p, i)
        self._taken = list()

    def select(self, k=2):
        """Select k chromosomes from the selection pool.

        TODO:
        - Prevent multiple selection of the same chromosomes.
        - Return string and no fitness.

        Args:
            k (int): Number of chromosomes to select.

        Returns: tuple list
        """
        parents = list()
        for _ in range(k):
            p = random.random()
            parent = None
            for i in range(len(self._selection_pool)):
                if self._selection_pool[i][1] < p:
                    parent = self._selection_pool[i]
                else:
                    self._taken.append(i-1)
                    break

            parents.append(parent)

        return parents


def genetic_algorithm(G, max_steps=100, pop_size=100, operator=single_point_crossover,
                      selection_process_cls=TournamentSelection, p_gen=(0.2, 0.5), p_operator=1):
    """Tries to resolve the minimum Steiner tree problem with a genetic algorithm

    Args:
        G (networkx.Graph): Graph of the problem.
        max_steps (int): Maximum number of steps of the algorithm.
        pop_size (int): Population size.
        operator (function): Operator used.
        selection_process_cls: Selection process used.
        p_gen (float or tuple): Proportion of bits to 1; used for the generation
            of the initial population.
        p_operator (float): Probability for the operator to have an effect on the
            selected parents.

    Returns: (float)
        Approximation of the optimal solution
    """
    solution_size = gt.size_of_solution(G)
    population = full_generation(pop_size, solution_size, p_gen)
    population_fitness = {population[i]: 1/gt.fitness_evaluation(population[i], G) for i in range(pop_size)}
    sorted_pop_fitness = None

    print("Generated {} random starting candidate solutions".format(len(population)))

    for _ in range(max_steps):
        new_pop_fitness = dict()

        sorted_pop_fitness = sorted(population_fitness.items(), key=itemgetter(1), reverse=True)
        selection_process = selection_process_cls(solutions=sorted_pop_fitness)

        for _i in range(int(pop_size/2)):
            # parents = random.choices(sorted_pop_fitness[:int(pop_size*0.1)], k=2)
            parents = selection_process.select(k=2)
            child1, child2 = operator(parents[0][0], parents[1][0], p_operator)
            child1_m = mutation(child1)
            child2_m = mutation(child2)
            results = sorted([(parents[0][0], population_fitness[parents[0][0]]),
                              (parents[1][0], population_fitness[parents[1][0]]),
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
    graph = gt.graph_loader("B/b15.stp")
    solution = genetic_algorithm(graph)
    solution_graph = gt.kruskal(gt.build_graph_of_solution(solution[0], graph))
    print("Solution cost = {}".format(gt.fitness_evaluation(solution[0], graph)))
    draw_graph(solution_graph)