from django.db import models


class Torneo(models.Model):
    # Ya no usamos ForeignKey a User, solo nombres para juego rápido
    jugador1_nombre = models.CharField(max_length=50)
    jugador2_nombre = models.CharField(max_length=50)

    # Marcador global de la sesión
    puntuacion_j1 = models.IntegerField(default=0)
    puntuacion_j2 = models.IntegerField(default=0)
    empates = models.IntegerField(default=0)

    # Datos para tus futuras métricas (Punto 5)
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    fecha_fin = models.DateTimeField(null=True, blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"Torneo: {self.jugador1_nombre} vs {self.jugador2_nombre}"


class Partida(models.Model):
    # Cada partida pertenece a un torneo
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