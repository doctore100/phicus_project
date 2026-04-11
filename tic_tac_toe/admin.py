from django.contrib import admin
from .models import Torneo, Partida


@admin.register(Torneo)
class TorneoAdmin(admin.ModelAdmin):
    # Añadimos 'empates' para que coincida exactamente con las métricas del Dashboard
    list_display = ('id', 'jugador1_nombre', 'jugador2_nombre', 'puntuacion_j1', 'puntuacion_j2', 'empates', 'activo',
                    'fecha_inicio')

    # Filtros laterales
    list_filter = ('activo', 'fecha_inicio')

    # Barra de búsqueda
    search_fields = ('jugador1_nombre', 'jugador2_nombre')

    # Ordenar igual que en el Dashboard (los más recientes primero)
    ordering = ('-fecha_inicio',)


@admin.register(Partida)
class PartidaAdmin(admin.ModelAdmin):
    list_display = ('id', 'torneo', 'estado', 'ganador', 'fecha_creacion')

    # Añadimos fecha_creacion a los filtros para buscar partidas de un día específico
    list_filter = ('estado', 'ganador', 'fecha_creacion')

    # Búsqueda relacional: Buscar partidas por el nombre de los jugadores del torneo
    search_fields = ('torneo__jugador1_nombre', 'torneo__jugador2_nombre')

    # Ordenar las partidas más recientes primero
    ordering = ('-fecha_creacion',)