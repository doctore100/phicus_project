from django.contrib import admin
from .models import Torneo, Partida

@admin.register(Torneo)
class TorneoAdmin(admin.ModelAdmin):
    # Columnas que se verán en la tabla principal
    list_display = ('id', 'jugador1_nombre', 'jugador2_nombre', 'puntuacion_j1', 'puntuacion_j2', 'activo')
    # Filtros laterales automáticos
    list_filter = ('activo', 'fecha_inicio')
    # Barra de búsqueda
    search_fields = ('jugador1_nombre', 'jugador2_nombre')

@admin.register(Partida)
class PartidaAdmin(admin.ModelAdmin):
    list_display = ('id', 'torneo', 'estado', 'ganador', 'fecha_creacion')
    list_filter = ('estado', 'ganador')