from django.urls import path
from . import views

urlpatterns = [
    path('', views.iniciar_torneo, name='iniciar_torneo'),
    path('torneo/<int:torneo_id>/partida/<int:partida_id>/', views.jugar_partida, name='jugar_partida'),
]