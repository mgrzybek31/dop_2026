from dataclasses import dataclass
import matplotlib.pyplot as plt

from .species import Creature, Prey, Predator


@dataclass
class HistoryElement:
    prey: int
    predators: int

class Population:

    _instances: dict[Prey: set, Predator: set]
    history: dict[Prey: list, Predator: list]

    def __init__(self, n_prey: int, n_predator: int, **kwargs):

        self._instances = set(
            [Creature(**kwargs) for _ in range(n)]
        )

        self.history = [self.n]

    def natural_selection(self):

        newborns = set()
        for creature in self._instances:
            new_one = creature.reproduce()


        for creature in self._instances:
            creature.kill()

        ## iteruj po tym czego jest wiecej przy polowaniu
        #if self.__name__ == Predator:
            #poluj
        #    pass
        ## jezeli predatorow jest wiecej niz prey to iteruj po wszytskich predatorach (modulo) dopoki sa wolne prey (predator ma 1 szanse na zapolowanie w jednej selekcji naturalnje)
        ## jezeli prey jest wiecej niz predatorow to tez iteruj po predatorach, jesli ktoremus sie nie udalo to ma druga szanse (bo wiecej prey), mozna losowac prey dla predatora,
        """
        permutacja prey zeby bylo losowo (opcjonalnie)
        for i in predator:
            aktualizuj prey - wywalaj not alive zeby predator nie polowal na martwe
        """

        self._instances = set([creature for creature in self._instances if creature.alive])

        self.history.append(self.n)

    def plot_history(self):
        plt.plot(self.history)
        plt.xlabel("Pokolenie")
        plt.ylabel("Liczebność populacji")
        plt.title("Historia populacji")
        plt.show()

    @property
    def n(self):
        return len(self._instances)
