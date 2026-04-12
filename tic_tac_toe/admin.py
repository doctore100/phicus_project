from django.contrib import admin
from .models import Tournament, Match


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    # Añadimos 'draws' para que coincida exactamente con las métricas del Dashboard
    list_display = ('id', 'player1_name', 'player2_name', 'score_p1', 'score_p2', 'draws', 'is_active',
                    'started_at')

    # Filtros laterales
    list_filter = ('is_active', 'started_at')

    # Barra de búsqueda
    search_fields = ('player1_name', 'player2_name')

    # Ordenar igual que en el Dashboard (los más recientes primero)
    ordering = ('-started_at',)


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('id', 'tournament', 'status', 'winner', 'created_at')

    # Añadimos created_at a los filtros para buscar partidas de un día específico
    list_filter = ('status', 'winner', 'created_at')

    # Búsqueda relacional: Buscar partidas por el nombre de los jugadores del torneo
    search_fields = ('tournament__player1_name', 'tournament__player2_name')

    # Ordenar las partidas más recientes primero
    ordering = ('-created_at',)