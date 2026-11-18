"""Define organisms and their behavior in the predator-prey simulation."""

import random
from typing import Self


class Probability:
    """Store an instance probability clamped to the interval [0, 1]."""

    def __set_name__(self, owner: type[object], name: str) -> None:
        """
        Set the private attribute name used to store the probability.

        :param type[object] owner: class that defines the descriptor
        :param str name: public name of the probability attribute
        """

        self.storage_name: str = f"_{owner.__name__}__{name}"

    def __get__(self, instance: object | None, owner: type[object]):
        """
        Return the stored probability, or the descriptor on class access.

        :param object | None instance: object being read, or None for class access
        :param type[object] owner: class through which the attribute is accessed
        """

        if instance is None:
            return self
        return getattr(instance, self.storage_name)

    def __set__(self, instance: object, value: float) -> None:
        """
        Clamp the probability to [0, 1] and store it on the instance.

        :param object instance: object whose probability is being set
        :param float value: probability before clamping
        """

        setattr(instance, self.storage_name, min(1.0, max(0.0, value)))


class Creature:
    """An organism that can die or reproduce according to its probabilities."""

    alive: bool = True
    default_p_death: float = 0.4
    default_p_reproduce: float = 0.5
    p_death: Probability = Probability()
    p_reproduce: Probability = Probability()

    def __init__(self, p_death: float | None = None, p_reproduce: float | None = None) -> None:
        """
        Initialize the probabilities of death and reproduction.
        
        :param float | None p_death: probability of death
        :param float | None p_reproduce: probability of reproduction
        """

        self.p_death = self.default_p_death if not p_death else p_death
        self.p_reproduce = self.default_p_reproduce if not p_reproduce else p_reproduce

    def kill(self) -> None:
        """Mark the creature as dead if death happens."""

        if random.random() < self.p_death:
            self.alive = False

    def reproduce(self) -> Self | None:
        """Return a new creature of the same species if reproduction succeeds."""

        if self.alive and (random.random() < self.p_reproduce):
            return self._create_offspring()

        return None

    def _create_offspring(self) -> Self:
        """
        Create an offspring that inherits the parents probabilities.

        :return: new creature of the same type as the parent
        """

        return self.__class__(p_death=self.p_death, p_reproduce=self.p_reproduce)


class Prey(Creature):
    """A creature with a probability of being hunted."""

    default_p_hunt: float = 0.5
    p_hunt: Probability = Probability()

    def __init__(self, p_death: float | None = None, p_reproduce: float | None = None, p_hunt: float | None = None) -> None:
        """
        Initialize the base probabilities and the probability of being hunted.

        :param float | None p_death: probability of death
        :param float | None p_reproduce: probability of reproduction
        :param float | None p_hunt: probability of being hunted
        """

        super().__init__(p_death, p_reproduce)
        self.p_hunt = self.default_p_hunt if not p_hunt else p_hunt

    def _create_offspring(self) -> Self:
        """
        Create an offspring that inherits the parent's probabilities.

        :return: new prey of the same type as the parent
        """

        return self.__class__(p_death=self.p_death, p_reproduce=self.p_reproduce, p_hunt=self.p_hunt)


class Predator(Creature):
    """A creature that hunts prey and whose mortality depends on hunger."""

    p_death_hungry: float = 0.9
    default_p_death: float = p_death_hungry

    def __init__(self, p_reproduce: float | None = None, hungry: bool = True, p_death: float | None = None) -> None:
        """
        Initialize the base probabilities and the starting hunger state.

        :param float | None p_reproduce: probability of reproduction
        :param bool hungry: whether the predator starts hungry
        :param float | None p_death: probability of death when not hungry
        """

        super().__init__(p_death, p_reproduce)
        self.hungry: bool = hungry

    def hunt(self, prey: Prey) -> None:
        """
        Kill the prey on a successful hunt and update the hunger state.

        :param Prey prey: prey encountered by the predator
        """

        if self.hungry and random.random() < prey.p_hunt:
            prey.alive = False
            self.hungry = False
        else:
            self.hungry = True

    def kill(self) -> None:
        """
        Use probability of hunger death when hungry
            and ordinary probability of death otherwise.
        """

        probability = self.p_death_hungry if self.hungry else self.p_death
        if random.random() < probability:
            self.alive = False
