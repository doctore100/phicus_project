from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .models import Torneo, Partida


def check_winner(board_str):
    combinations = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Horizontales
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Verticales
        (0, 4, 8), (2, 4, 6)  # Diagonales
    ]
    for a, b, c in combinations:
        if board_str[a] != '-' and board_str[a] == board_str[b] == board_str[c]:
            return board_str[a]
    if '-' not in board_str:
        return 'Empate'
    return None


def iniciar_torneo(request):
    """ Vista para ingresar los nombres sin login y empezar el torneo """
    if request.method == 'POST':
        j1 = request.POST.get('jugador1')
        j2 = request.POST.get('jugador2')

        # Creamos el torneo
        torneo = Torneo.objects.create(jugador1_nombre=j1, jugador2_nombre=j2)

        # Creamos la primera partida (ronda 1) de este torneo
        partida = Partida.objects.create(torneo=torneo)

        return redirect('jugar_partida', torneo_id=torneo.id, partida_id=partida.id)

    return render(request, 'tictactoe/setup.html')


def jugar_partida(request, torneo_id, partida_id):
    """ Vista del Couch Multiplayer (Mis pantalla) """
    torneo = get_object_or_404(Torneo, id=torneo_id)
    partida = get_object_or_404(Partida, id=partida_id)

    if request.method == 'POST':
        # Si presionaron el botón de "Siguiente Ronda"
        if 'siguiente_ronda' in request.POST:
            nueva_partida = Partida.objects.create(torneo=torneo)
            return redirect('jugar_partida', torneo_id=torneo.id, partida_id=nueva_partida.id)

        # Si presionaron "Terminar Torneo"
        if 'terminar_torneo' in request.POST:
            torneo.activo = False
            torneo.fecha_fin = timezone.now()
            torneo.save()
            return redirect('iniciar_torneo')  # Luego lo mandaremos a tu panel de métricas

        # Lógica de juego (clic en casilla)
        if partida.estado == 'en_curso':
            cell = request.POST.get('cell')
            if cell is not None:
                cell = int(cell)
                board_list = list(partida.tablero)

                # Ya no validamos el usuario, cualquiera puede jugar el turno
                if board_list[cell] == '-':
                    board_list[cell] = partida.turno_actual
                    partida.tablero = "".join(board_list)

                    ganador = check_winner(partida.tablero)
                    if ganador:
                        partida.estado = 'finalizada'
                        partida.ganador = ganador

                        # ¡Actualizamos las métricas del Torneo!
                        if ganador == 'X':
                            torneo.puntuacion_j1 += 1
                        elif ganador == 'O':
                            torneo.puntuacion_j2 += 1
                        else:
                            torneo.empates += 1
                        torneo.save()
                    else:
                        partida.turno_actual = 'O' if partida.turno_actual == 'X' else 'X'

                    partida.save()

    return render(request, 'tictactoe/board.html', {'torneo': torneo, 'partida': partida})


@staff_member_required(login_url='/admin/login/')
def dashboard_metricas(request):
    """ Vista analítica protegida: Panel de control de métricas globales """

    # 1. Métricas Generales (Cantidades totales)
    total_torneos = Torneo.objects.count()
    torneos_activos = Torneo.objects.filter(activo=True).count()
    total_partidas = Partida.objects.count()

    # 2. Agregaciones Matemáticas (Extrayendo totales)
    agregados = Torneo.objects.aggregate(
        victorias_j1=Sum('puntuacion_j1'),
        victorias_j2=Sum('puntuacion_j2'),
        total_empates=Sum('empates')
    )

    # Limpieza de nulos a ceros
    victorias_x = agregados['victorias_j1'] or 0
    victorias_o = agregados['victorias_j2'] or 0
    empates = agregados['total_empates'] or 0

    # --- MEJORA: Cálculo de Tasa de Victoria (Win Rate) ---
    total_juegos_validos = victorias_x + victorias_o + empates
    if total_juegos_validos > 0:
        win_rate_x = round((victorias_x / total_juegos_validos) * 100, 1)
        win_rate_o = round((victorias_o / total_juegos_validos) * 100, 1)
    else:
        win_rate_x = win_rate_o = 0

    # 3. Historial para la tabla: Los últimos 10 torneos (ampliado)
    ultimos_torneos = Torneo.objects.all().order_by('-fecha_inicio')[:10]

    # 4. Empaquetado del Contexto (Limpieza visual de variables)
    contexto = {
        'total_torneos': total_torneos,
        'torneos_activos': torneos_activos,
        'total_partidas': total_partidas,
        'victorias_x': victorias_x,
        'victorias_o': victorias_o,
        'empates': empates,
        'win_rate_x': win_rate_x,
        'win_rate_o': win_rate_o,
        'ultimos_torneos': ultimos_torneos,
    }

    return render(request, 'tictactoe/dashboard.html', contexto)
