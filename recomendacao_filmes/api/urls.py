from django.urls import path
from .views import recomendar_filmes

urlpatterns = [
    path('recomendar/', recomendar_filmes),
]