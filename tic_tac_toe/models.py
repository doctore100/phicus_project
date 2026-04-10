from django.db import models


class Torneo(models.Model):
    """
    Represents a tournament between two players.

    This class is used to track the details of a tournament, including player names,
    scores for each player, the number of ties, start and end dates, and the active
    status of the tournament.

    :ivar jugador1_nombre: Name of the first player.
    :type jugador1_nombre: str
    :ivar jugador2_nombre: Name of the second player.
    :type jugador2_nombre: str
    :ivar puntuacion_j1: Total score of the first player.
    :type puntuacion_j1: int
    :ivar puntuacion_j2: Total score of the second player.
    :type puntuacion_j2: int
    :ivar empates: Number of ties in the tournament.
    :type empates: int
    :ivar fecha_inicio: Start date and time of the tournament.
    :type fecha_inicio: datetime
    :ivar fecha_fin: End date and time of the tournament, if applicable.
    :type fecha_fin: datetime or None
    :ivar activo: Indicates whether the tournament is currently active.
    :type activo: bool
    """

    jugador1_nombre = models.CharField(max_length=50)
    jugador2_nombre = models.CharField(max_length=50)

    # Marcador global de la sesión
    puntuacion_j1 = models.IntegerField(default=0)
    puntuacion_j2 = models.IntegerField(default=0)
    empates = models.IntegerField(default=0)

    # Datos para tus futuras métricas y análisis de torneos
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    fecha_fin = models.DateTimeField(null=True, blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"Torneo: {self.jugador1_nombre} vs {self.jugador2_nombre}"


class Partida(models.Model):
    """
    Representation of a game (Partida) linked to a tournament (Torneo).

    This class is used to define a game instance within a tournament, keeping track of
    game attributes such as the current game state, board status, current turn, and
    winner. It also includes metadata such as the creation date.

    :ivar torneo: Reference to the tournament (Torneo) this game is associated with.
    :type torneo: Torneo
    :ivar tablero: Current state of the board represented as a string (e.g., "X-O-X----").
    :type tablero: str
    :ivar turno_actual: Current turn indicator, either 'X' or 'O'.
    :type turno_actual: str
    :ivar estado: Current state of the game. Possible values are 'en_curso' (in progress)
        or 'finalizada' (finished).
    :type estado: str
    :ivar ganador: Winner of the game, which can either be 'X', 'O', or 'Empate'
        (indicating a draw). Can be null if the game is still in progress.
    :type ganador: str or None
    :ivar fecha_creacion: Timestamp of when the game instance was created.
    :type fecha_creacion: datetime
    """
    torneo = models.ForeignKey(Torneo, on_delete=models.CASCADE, related_name='partidas')

    # Estado del tablero ("X-O-X----")
    tablero = models.CharField(max_length=9, default='---------')
    turno_actual = models.CharField(max_length=1, default='X')

    estado = models.CharField(max_length=20, default='en_curso')  # 'en_curso', 'finalizada'

    # Puede ser 'X' (Gana J1), 'O' (Gana J2), o 'Empate'
    ganador = models.CharField(max_length=10, null=True, blank=True)

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ronda de {self.torneo.jugador1_nombre} vs {self.torneo.jugador2_nombre}"