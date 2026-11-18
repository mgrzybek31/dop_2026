"""Run and compare predator-prey simulation scenarios."""

import random
from statistics import mean, stdev

from .population import Population
from .species import Prey, Predator

STEPS: int = 150
SEEDS: range = range(10)
BASE_REPRODUCE: float = 0.4
BASE_HUNT: float = 0.5


def simulate(seed: int, p_reproduce: float, p_hunt: float) -> Population:
	"""
	Run one simulation with the given seed and prey probabilities.

	:param int seed: seed for the random number generator
	:param float p_reproduce: reproduction probability for prey
	:param float p_hunt: probability of prey being caught in an encounter
	:return: population after all steps, including its recorded history
	"""

	old_reproduce, old_hunt = Prey.default_p_reproduce, Prey.default_p_hunt
	random_state = random.getstate()
	try:
		Prey.default_p_reproduce = p_reproduce
		Prey.default_p_hunt = p_hunt
		random.seed(seed)
		population = Population({Prey: 30, Predator: 30})
		for _ in range(STEPS):
			population.natural_selection()
		return population
	finally:
		Prey.default_p_reproduce = old_reproduce
		Prey.default_p_hunt = old_hunt
		random.setstate(random_state)


def report(label: str, runs: list[Population]) -> None:
	"""
	Print the extinction rate, mean, and sample standard deviation for each species.

	:param str label: name of the scenario being reported
	:param list[Population] runs: at least two completed runs of the scenario
	"""

	final_counts = [population.n for population in runs]
	print(f"\n{label} ({len(runs)} prob, krok {STEPS})")
	for species in (Prey, Predator):
		counts = [result[species] for result in final_counts]
		extinction_percent = 100 * counts.count(0) / len(counts)
		print(f"  {species.__name__}: wymarcie {extinction_percent:.0f}%, "
			  f"mean: {mean(counts):.2f}, std: {stdev(counts):.2f}")


def main() -> None:
	"""Run the baseline and sensitivity experiments, then show the plots."""

	baseline = [simulate(seed, BASE_REPRODUCE, BASE_HUNT) for seed in SEEDS]
	repeated = simulate(SEEDS[0], BASE_REPRODUCE, BASE_HUNT)
	assert baseline[0].history == repeated.history and baseline[0].n == repeated.n
	print(f"Powtarzalnosc: identyczna historia i wynik dla ziarna {SEEDS[0]}.")
	report(f"Baza: p_reproduce={BASE_REPRODUCE}, p_hunt={BASE_HUNT}", baseline)
	baseline[0].plot_history("Scenariusz bazowy")

	for p_reproduce in (0.25, 0.30, 0.35):
		label = f"Prey.default_p_reproduce={p_reproduce:.2f}"
		runs = [simulate(seed, p_reproduce, BASE_HUNT) for seed in SEEDS]
		report(label, runs)
		runs[0].plot_history(label)
	for p_hunt in (0.20, 0.35, 0.70):
		label = f"Prey.default_p_hunt={p_hunt:.2f}"
		runs = [simulate(seed, BASE_REPRODUCE, p_hunt) for seed in SEEDS]
		report(label, runs)
		runs[0].plot_history(label)

	histogram_seed, histogram_run = next(
		((seed, run) for seed, run in zip(SEEDS, baseline) if any(run.n.values())),
		(SEEDS[0], baseline[0]),
	)
	print(f"\nHistogram p_reproduce: scenariusz bazowy, ziarno {histogram_seed}.")
	histogram_run.plot_histogram("p_reproduce")


if __name__ == "__main__":
	main()
