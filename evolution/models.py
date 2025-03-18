from math import sqrt
from core.util import generate_normalized_value, generate_random_delta


class Individual:
    def __init__(self, lifespan, strength=None, speed=None, intelligence=None):
        self.strength = strength if strength else generate_normalized_value()
        self.speed = speed if speed else generate_normalized_value()
        self.intelligence = intelligence if intelligence else generate_normalized_value()
        self.fitness = 0
        self.update_fitness()
        self.age = 0
        self.lifespan = lifespan

    def update_fitness(self):
        self.fitness = 0.3 * self.strength + 0.3 * self.speed + 0.4 * self.intelligence

    def is_alive(self):
        return self.age < self.lifespan

    def mutate(self):
        self.strength += generate_random_delta()
        self.speed += generate_random_delta()
        self.intelligence += generate_random_delta()

        self.strength = max(0, min(self.strength, 1))
        self.speed = max(0, min(self.speed, 1))
        self.intelligence = max(0, min(self.intelligence, 1))
        self.update_fitness()



class Population:
    def __init__(self, size, lifespan, fit_threshold):
        self.individuals = [Individual(lifespan) for _ in range(size)]
        self.fit_threshold = fit_threshold
        self.average_fitness = None
        self.num = size

    def evolve(self):
        new_average_fitness = 0
        new_num = 0

        parents = []

        for individual in self.individuals:
            individual.age += 1
            if individual.is_alive():
                parents.append(individual)
                new_average_fitness += individual.fitness
                new_num += 1

        parents.sort(key=lambda x: x.fitness, reverse=True)

        next_generation = parents
        for i in range(0, len(parents) - 1, 2):
            parent1, parent2 = parents[i], parents[i + 1]
            if parent1.fitness > self.fit_threshold and parent2.fitness > self.fit_threshold:

                strength = (parent1.strength + parent2.strength) / 2
                speed = (parent1.speed + parent2.speed) / 2
                intelligence = (parent1.intelligence + parent2.intelligence) / 2
                child = Individual(lifespan=parent1.lifespan, strength=strength, speed=speed, intelligence=intelligence)
                child.mutate()
                next_generation.append(child)
                new_average_fitness += child.fitness
                new_num += 1
            else:
                break

        self.individuals = next_generation
        self.average_fitness = new_average_fitness / new_num if new_num else None
        self.num = new_num

    def get_sd(self):
        n = self.num
        if n == 1:
            return None
        mean = self.average_fitness
        square_sum = 0
        for individual in self.individuals:
            square_sum += (mean - individual.fitness)**2
        return sqrt(square_sum / (n - 1))
