from django.contrib import admin
from django.urls import include, path
from api import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('recomendar/', views.recomendar_filmes, name='recomendar'),
]
