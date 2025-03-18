from logging import getLogger
from .models import Population

logger = getLogger(__name__)


class Simulation:
    def __init__(self, size, lifespan, fit_threshold, num_generations=100):
        self.pop = Population(size=size, lifespan=lifespan, fit_threshold=fit_threshold)
        self.pop.save()
        self.generations = num_generations
        logger.debug(f"Simulation object created! Params: size - {self.pop.size}, lifespan - {self.pop.lifespan}, fit_threshold - {self.pop.fit_threshold}, num_generations - {num_generations}")

    def run(self):
        for generation in range(self.generations):
            logger.debug(
                f"Simulation is about to evolve! Params: size - {self.pop.size}, lifespan - {self.pop.lifespan}, fit_threshold - {self.pop.fit_threshold}")
            self.pop.evolve()
            logger.debug(
                f"Simulation evolved! Params: size - {self.pop.size}, lifespan - {self.pop.lifespan}, fit_threshold - {self.pop.fit_threshold}")

            if self.pop.size:
                avg_fitness = self.pop.average_fitness
                avg_fitness_str = f"{avg_fitness:.4f}" if avg_fitness else "no date"
                dispersion = self.pop.get_sd()
                disp_str = f"{dispersion:.4f}" if dispersion else "no data"
                print(f"Generation {generation + 1}, Average Fitness: " + avg_fitness_str + " Dispersion: " + disp_str)
            else:
                print("Everyone died!")
                break
