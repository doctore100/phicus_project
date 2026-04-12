from django.urls import path
from . import views

urlpatterns = [
    # Inicio del juego
    path('', views.start_tournament, name='start_tournament'),

    # Tablero de juego interactivo
    path('tournament/<int:tournament_id>/match/<int:match_id>/', views.play_match, name='play_match'),

    # Panel de analítica
    path('dashboard/', views.metrics_dashboard, name='metrics_dashboard'),
]