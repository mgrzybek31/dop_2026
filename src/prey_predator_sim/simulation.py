from population import Population
from species import Prey, Predator

prey_population = Population(Prey, 100, p_death=0.4, p_reproduce=0.5, p_hunt=0.5)
predator_population = Population(Predator, 100, p_reproduce=0.5, hungry=True)

