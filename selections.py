import random


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
                    parent = candidate[0]
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
                    parent = self._selection_pool[i][0]
                else:
                    self._taken.append(i - 1)
                    break

            parents.append(parent)

        return parents


selections = {
    'fitness_proportionate': FitnessProportionateSelection,
    'tournament': TournamentSelection
}