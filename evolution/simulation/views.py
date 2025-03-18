from django.shortcuts import render
from .simulator import Simulation


def index(request):
    return render(request, 'index.html')


def run_simulation(request):
    if request.method == 'POST':
        size = int(request.POST["size"])
        lifespan = int(request.POST["lifespan"])
        fit_threshold = float(request.POST["fit_threshold"])
        num_generations = int(request.POST["num_generations"])

        sim = Simulation(
            size=size,
            lifespan=lifespan,
            fit_threshold=fit_threshold,
            num_generations=num_generations,
        )
        sim.run()

        return render(request, 'output.html')
