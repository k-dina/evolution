from models import Population


class Simulation:
    def __init__(self, size, lifespan, generations, fit_threshold):
        self.pop = Population(size, lifespan, fit_threshold)
        self.generations = generations

    def run(self):
        for generation in range(self.generations):
            self.pop.evolve()
            if self.pop.num:
                avg_fitness = self.pop.average_fitness
                avg_fitness_str = f"{avg_fitness:.4f}" if avg_fitness else "no date"
                dispersion = self.pop.get_sd()
                disp_str = f"{dispersion:.4f}" if dispersion else "no data"
                print(f"Generation {generation + 1}, Average Fitness: " + avg_fitness_str + " Dispersion: " + disp_str)
            else:
                print("Everyone died!")
                break


sim = Simulation(size=100, lifespan=3, generations=1000, fit_threshold=0.5)
sim.run()