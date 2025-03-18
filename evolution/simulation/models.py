from logging import getLogger
from math import sqrt
from django.db import models
from .util import generate_random_delta, generate_normalized_value

logger = getLogger(__name__)


class Population(models.Model):
    size = models.IntegerField()
    lifespan = models.IntegerField()
    fit_threshold = models.FloatField()
    average_fitness = models.FloatField(null=True, blank=True)

    def generate_population(self):
        for _ in range(self.size):
            individual = Individual(population=self)
            individual.save()

    def evolve(self):
        new_average_fitness = 0
        new_num = 0

        parents = []

        individuals = Individual.objects.filter(population=self)

        for individual in individuals:
            individual.age += 1
            individual.save()
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
                child = Individual.objects.create(
                    strength=strength,
                    speed=speed,
                    intelligence=intelligence,
                    population=self
                )
                child.mutate()
                next_generation.append(child)
                new_average_fitness += child.fitness
                new_num += 1
            else:
                break

        Individual.objects.filter(population=self).exclude(pk__in=[ind.pk for ind in next_generation]).delete()

        self.average_fitness = new_average_fitness / new_num if new_num else None
        self.size = new_num
        self.save()

    def get_sd(self):
        n = self.size
        if n == 1:
            return None
        mean = self.average_fitness
        square_sum = 0
        individuals = Individual.objects.filter(population=self)
        for individual in individuals:
            square_sum += (mean - individual.fitness) ** 2
        return sqrt(square_sum / (n - 1))

    def __str__(self):
        return f"Population(id={self.pk}, size={self.size}, lifespan={self.lifespan})"


class Individual(models.Model):
    strength = models.FloatField(default=generate_normalized_value)
    speed = models.FloatField(default=generate_normalized_value)
    intelligence = models.FloatField(default=generate_normalized_value)
    fitness = models.FloatField(default=0)
    age = models.IntegerField(default=0)
    population = models.ForeignKey(
        Population,
        on_delete=models.CASCADE,
        related_name='individuals'
    )

    def update_fitness(self):
        self.fitness = 0.3 * self.strength + 0.3 * self.speed + 0.4 * self.intelligence

    def is_alive(self):
        return self.age < self.population.lifespan

    def mutate(self):
        self.strength += generate_random_delta()
        self.speed += generate_random_delta()
        self.intelligence += generate_random_delta()

        self.strength = max(0, min(self.strength, 1))
        self.speed = max(0, min(self.speed, 1))
        self.intelligence = max(0, min(self.intelligence, 1))
        self.save()

    def save(self, *args, **kwargs):
        self.update_fitness()
        super().save(*args, **kwargs)
