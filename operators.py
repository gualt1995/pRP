import random


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
    if p < p_crossover:
        index = random.randint(0, len(parent1))
        firstpar1, secondpar1 = parent1[:index], parent1[index:]
        firstpar2, secondpar2 = parent2[:index], parent2[index:]
        parent1 = firstpar1 + secondpar2
        parent2 = firstpar2 + secondpar1
    return parent1, parent2


def uniform_crossover(parent1, parent2, p):
    TRESHOLD = 0.5
    child1 = ""
    child2 = ""
    for i in range(len(parent1)):
        p1 = random.random()
        p2 = random.random()
        child1 += parent1[i] if p1 < TRESHOLD else parent2[i]
        child2 += parent1[i] if p2 < TRESHOLD else parent2[i]

    return child1, child2


def uniform_mutation(solution):
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
        if random.random() < 1/len(solution):
            if bit == "0":
                res += "1"
            else:
                res += "0"
        else:
            res += bit
    return res


operators = {
    'uniform_mutation': uniform_mutation,
    'single_point_crossover': single_point_crossover,
    'uniform_crossover': uniform_crossover
}