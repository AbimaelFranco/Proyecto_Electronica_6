from django.urls import path
from ProyectoApp import views

urlpatterns = [
    path('', views.home, name="Home"),
    path('live', views.graph_live, name="Live"),
    path('history', views.graph_history, name="History"),
]