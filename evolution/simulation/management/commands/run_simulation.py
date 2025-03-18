from logging import getLogger
from django.core.management.base import BaseCommand
from ...simulator import Simulation

logger = getLogger(__name__)


class Command(BaseCommand):
    help = 'Runs the simulation'

    def add_arguments(self, parser):
        parser.add_argument('size', type=int, help='Population size')
        parser.add_argument('lifespan', type=int, help='Lifespan')
        parser.add_argument('fit_threshold', type=float, help='Fitness threshold')
        parser.add_argument('num_generations', type=int, help='Number of generations')

    def handle(self, *args, **options):
        size = options['size']
        lifespan = options['lifespan']
        fit_threshold = options['fit_threshold']
        num_generations = options['num_generations']
        logger.debug(f"Starting simulation with size={size}, lifespan={lifespan}, fit_threshold={fit_threshold}, num_generations={num_generations}")

        sim = Simulation(size=size, lifespan=lifespan, fit_threshold=fit_threshold, num_generations=num_generations)
        sim.run()
