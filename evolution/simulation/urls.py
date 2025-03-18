from django.urls import path
from . import views

app_name = 'simulation'

urlpatterns = [
    path('', views.index, name='index'),
    path('run/', views.run_simulation, name='run_simulation'),
]