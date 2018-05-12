import random
from operator import itemgetter


class FitnessProportionateSelection:
    """Implements a fitness proportionate selection process.
    The selection pool is constructed as a list usable by the
    `Selection.select` function.
    """

    def __init__(self, **kwargs):
        """Construct the selection pool, a list of tuples sorted by
        cumulative fitness.

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

    def select(self, k=2):
        """Select k chromosomes from the selection pool.

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
                    parent = candidate[0]
                else:
                    break
            parents.append(parent)

        return parents


class TournamentSelection:
    """Implements a tournament selection. The probability of being chosen
    is highest for the best solution and decreases exponentially for the lower
    ranks.

    Attributes:
        DEFAULT_PROBABILITY (float): Default base probability of being chosen for
            the best solution.
        DEFAULT_TOURNAMENT_PROP (float): Default proportion of solutions used in
            the tournament.
    """
    DEFAULT_PROBABILITY = 0.3
    DEFAULT_PROPORTION = 0.7

    def __init__(self, **kwargs):
        """

        Args:
            solutions (tuple list): List of candidate solutions with
                their associated fitness.
            p (float): Base probability of being chosen for the best solution.
                Defaults to 50% chance.
            size (int): Number of candidates to be chosen in the tournament.
        """
        self.p = kwargs.get('p', TournamentSelection.DEFAULT_PROBABILITY)
        self.tournament_size = kwargs.get('size', int(len(kwargs['solutions'])
                                                 * TournamentSelection.DEFAULT_PROPORTION))
        self.solutions = kwargs['solutions']


    def select(self, k=2):
        """Select k chromosomes from the selection pool.

        FIX:
        - If only one unique chromosome in selection pool...

        Args:
            k (int): Number of chromosomes to select.

        Returns: tuple list
        """
        self._selection_pool = list()
        if self.tournament_size == len(self.solutions):
            candidates = self.solutions
        else:
            candidates = sorted(random.sample(self.solutions, self.tournament_size),
                                key=itemgetter(1), reverse=True)

        cum_sum = 0
        for i in range(self.tournament_size):
            self._selection_pool.append((candidates[i][0], cum_sum))
            cum_sum += self.p * pow(1 - self.p, i)

        parents = list()
        for _ in range(k):
            p = random.random()
            parent = None
            for i in range(len(self._selection_pool)):
                if self._selection_pool[i][1] < p:
                    parent = self._selection_pool[i][0]
                else:
                    if parent in parents:
                        j = i - 1
                        while self._selection_pool[j][0] in parents:
                            j = len(self._selection_pool) - 1 if j-1 < 0 else j-1
                            # j = (j + 1) % len(self._selection_pool)
                        parent = self._selection_pool[j][0]
                    break
            parents.append(parent)

        assert(len(set(parents)) == 2)
        return parents


class SUSSelection:
    """Stochastic universal sampling"""

    def __init__(self, **kwargs):
        # Build cumulative fitness list..
        self._selection_pool = list()
        cum_sum = 0
        for s in kwargs['solutions']:
            cum_sum += s[1]
            self._selection_pool.append((s[0], cum_sum))
        self.fitness_sum = cum_sum

    def select(self, k=2):
        pointer_dst = self.fitness_sum / k
        start = random.uniform(0, pointer_dst)
        pointers = [start + i * pointer_dst for i in range(k)]
        return self._rws(pointers)

    def _rws(self, pointers):
        parents = list()
        for pointer in pointers:
            i = 0
            while self._selection_pool[i][1] < pointer:
                i += 1
            parents.append(self._selection_pool[i][0])
        return parents


selections = {
    'fitness_proportionate': FitnessProportionateSelection,
    'tournament': TournamentSelection,
    'sus': SUSSelection
}