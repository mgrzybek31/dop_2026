"""Manage a population and visualize the results of its evolution."""

import matplotlib.pyplot as plt

from .species import Creature, Prey, Predator


class Population:
    """Store creatures and keep track of the number of survivors by species."""

    def __init__(self, population_data: dict[type[Creature], int]) -> None:
        """
        Create the initial population.

        :param dict[type[Creature], int] population_data: initial count for each species
        """

        self._species: tuple[type[Creature], ...] = tuple(population_data)
        self._ordered_instances: list[Creature] = [
            species() for species, count in population_data.items() for _ in range(count)
        ]
        self._instances: set[Creature] = set(self._ordered_instances)
        self.history: list[dict[type[Creature], int]] = [self.n]

    def count_by_species(self) -> dict[type[Creature], int]:
        """
        Count the living creatures of each species.

        :return: number of living creatures of each species
        """

        counts = dict.fromkeys(self._species, 0)
        for creature in self._instances:
            if creature.alive:
                counts[type(creature)] += 1

        return counts

    @property
    def n(self) -> dict[type[Creature], int]:
        """
        Get the current population counts.

        :return: number of living creatures for each species
        """

        return self.count_by_species()

    def hunting(self) -> None:
        """Pair living predators and prey one to one and run each encounter."""

        predators = [creature for creature in self._ordered_instances if isinstance(creature, Predator) and creature.alive]
        prey = [creature for creature in self._ordered_instances if isinstance(creature, Prey) and creature.alive]

        for predator, victim in zip(predators, prey):
            predator.hunt(victim)

    def natural_selection(self) -> None:
        """
        Apply reproduction, hunting, and death for one step.

        Record survivor counts before removing dead creatures and adding newborns.
        """

        newborns = []
        for creature in self._ordered_instances:
            if creature.alive:
                newborn = creature.reproduce()
                if newborn is not None:
                    newborns.append(newborn)

        self.hunting()
        for creature in self._ordered_instances:
            if creature.alive:
                creature.kill()

        self._ordered_instances = [creature for creature in self._ordered_instances if creature.alive]
        self._ordered_instances.extend(newborns)
        self._instances = set(self._ordered_instances)
        self.history.append(self.n)

    def plot_history(self, title: str = "Historia populacji") -> None:
        """
        Show the recorded population counts by species and step.

        :param str title: title displayed above the plot
        """

        plt.figure()
        for species in self._species:
            sizes = [counts[species] for counts in self.history]
            plt.plot(sizes, label=species.__name__)
        plt.xlabel("Krok")
        plt.ylabel("Liczebność populacji")
        plt.title(title)
        plt.grid()
        if self._species:
            plt.legend()
        plt.show()

    def plot_histogram(self, attr: str) -> None:
        """
        Show the distribution of an attribute among living creatures that have it.

        :param str attr: name of the numeric attribute to plot
        """

        values = [getattr(creature, attr) for creature in self._instances if creature.alive and hasattr(creature, attr)]
        plt.figure()
        plt.hist(values)
        plt.xlabel(attr)
        plt.ylabel("Liczebność")
        plt.grid()
        plt.show()
