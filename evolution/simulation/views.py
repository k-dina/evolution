from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from io import StringIO
import logging
from .simulator import Simulation

logger = logging.getLogger(__name__)


def index(request):
    return render(request, 'index.html')


def run_simulation(request):
    if request.method == 'POST':
        size = int(request.POST['size'])
        lifespan = int(request.POST['lifespan'])
        fit_threshold = float(request.POST['fit_threshold'])
        num_generations = int(request.POST['num_generations'])

        log_stream = StringIO()
        handler = logging.StreamHandler(log_stream)
        logger.addHandler(handler)

        sim = Simulation(size=size, lifespan=lifespan, fit_threshold=fit_threshold, num_generations=num_generations)
        sim.run()

        logs = log_stream.getvalue().split('\n')
        logger.removeHandler(handler)

        return render(request, 'output.html', {'logs': logs})
    else:
        return HttpResponseRedirect(reverse('simulation:index'))
