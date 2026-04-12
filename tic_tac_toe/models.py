from django.db import models


class Tournament(models.Model):
    """
    Represents a tournament between two players.

    This class is used to track the details of a tournament, including player names,
    scores for each player, the number of ties, start and end dates, and the active
    status of the tournament.

    :ivar player1_name: Name of the first player.
    :type player1_name: str
    :ivar player2_name: Name of the second player.
    :type player2_name: str
    :ivar score_p1: Total score of the first player.
    :type score_p1: int
    :ivar score_p2: Total score of the second player.
    :type score_p2: int
    :ivar draws: Number of ties in the tournament.
    :type draws: int
    :ivar started_at: Start date and time of the tournament.
    :type started_at: datetime
    :ivar ended_at: End date and time of the tournament, if applicable.
    :type ended_at: datetime or None
    :ivar is_active: Indicates whether the tournament is currently active.
    :type is_active: bool
    """

    player1_name = models.CharField(max_length=50)
    player2_name = models.CharField(max_length=50)

    # Global scoreboard
    score_p1 = models.IntegerField(default=0)
    score_p2 = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)

    # Analytics data
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Tournament: {self.player1_name} vs {self.player2_name}"


class Match(models.Model):
    """
    Representation of a game (Match) linked to a tournament (Tournament).

    This class is used to define a game instance within a tournament, keeping track of
    game attributes such as the current game state, board status, current turn, and
    winner. It also includes metadata such as the creation date.

    :ivar tournament: Reference to the tournament this game is associated with.
    :type tournament: Tournament
    :ivar board: Current state of the board represented as a string (e.g., "X-O-X----").
    :type board: str
    :ivar current_turn: Current turn indicator, either 'X' or 'O'.
    :type current_turn: str
    :ivar status: Current state of the game. Possible values are 'in_progress' or 'completed'.
    :type status: str
    :ivar winner: Winner of the game, which can either be 'X', 'O', or 'Draw'.
        Can be null if the game is still in progress.
    :type winner: str or None
    :ivar created_at: Timestamp of when the game instance was created.
    :type created_at: datetime
    """
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='matches')

    # Board state ("X-O-X----")
    board = models.CharField(max_length=9, default='---------')
    current_turn = models.CharField(max_length=1, default='X')

    status = models.CharField(max_length=20, default='in_progress')  # 'in_progress', 'completed'

    # Can be 'X' (P1 wins), 'O' (P2 wins), or 'Draw'
    winner = models.CharField(max_length=10, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Round of {self.tournament.player1_name} vs {self.tournament.player2_name}"