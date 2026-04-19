import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from tic_tac_toe.models import Tournament, Match
from tic_tac_toe.views import check_winner

@pytest.mark.parametrize("board, expected", [
    ("XXX------", "X"),
    ("---OOO---", "O"),
    ("------XXX", "X"),
    ("X--X--X--", "X"),
    ("-O--O--O-", "O"),
    ("--X--X--X", "X"),
    ("X---X---X", "X"),
    ("--O-O-O--", "O"),
    ("XOXOXXOXO", "Draw"),
    ("XOX------", None),
    ("---------", None),
])
def test_check_winner(board, expected):
    assert check_winner(board) == expected

@pytest.mark.django_db
class TestTournament:
    def test_create_tournament(self):
        tournament = Tournament.objects.create(player1_name="Alice", player2_name="Bob")
        assert str(tournament) == "Tournament: Alice vs Bob"
        assert tournament.is_active is True
        assert tournament.score_p1 == 0
        assert tournament.score_p2 == 0
        assert tournament.draws == 0

    def test_start_tournament_view(self, client):
        url = reverse('start_tournament')
        response = client.get(url)
        assert response.status_code == 200

        response = client.post(url, {'player1': 'Alice', 'player2': 'Bob'})
        assert response.status_code == 302
        tournament = Tournament.objects.get(player1_name="Alice")
        match = Match.objects.get(tournament=tournament)
        assert response.url == reverse('play_match', kwargs={'tournament_id': tournament.id, 'match_id': match.id})

@pytest.mark.django_db
class TestMatch:
    @pytest.fixture
    def active_game(self):
        tournament = Tournament.objects.create(player1_name="Alice", player2_name="Bob")
        match = Match.objects.create(tournament=tournament)
        return tournament, match

    def test_create_match(self, active_game):
        tournament, match = active_game
        assert str(match) == f"Round of {tournament.player1_name} vs {tournament.player2_name}"
        assert match.board == "---------"
        assert match.current_turn == "X"
        assert match.status == "in_progress"

    def test_play_move(self, client, active_game):
        tournament, match = active_game
        url = reverse('play_match', kwargs={'tournament_id': tournament.id, 'match_id': match.id})
        
        # Player X moves to center
        response = client.post(url, {'cell': '4'})
        assert response.status_code == 200
        match.refresh_from_db()
        assert match.board[4] == 'X'
        assert match.current_turn == 'O'

    def test_win_game(self, client, active_game):
        tournament, match = active_game
        url = reverse('play_match', kwargs={'tournament_id': tournament.id, 'match_id': match.id})
        
        # X: 0, 1, 2
        # O: 3, 4
        moves = [0, 3, 1, 4, 2]
        for move in moves:
            client.post(url, {'cell': str(move)})
        
        match.refresh_from_db()
        tournament.refresh_from_db()
        assert match.status == 'completed'
        assert match.winner == 'X'
        assert tournament.score_p1 == 1

    def test_next_round(self, client, active_game):
        tournament, match = active_game
        url = reverse('play_match', kwargs={'tournament_id': tournament.id, 'match_id': match.id})
        
        response = client.post(url, {'next_round': 'true'})
        assert response.status_code == 302
        assert Match.objects.filter(tournament=tournament).count() == 2

    def test_end_tournament(self, client, active_game):
        tournament, match = active_game
        url = reverse('play_match', kwargs={'tournament_id': tournament.id, 'match_id': match.id})
        
        response = client.post(url, {'end_tournament': 'true'})
        assert response.status_code == 302
        tournament.refresh_from_db()
        assert tournament.is_active is False
        assert tournament.ended_at is not None

@pytest.mark.django_db
def test_metrics_dashboard_staff_only(client):
    url = reverse('metrics_dashboard')
    
    # Anonymous user should be redirected
    response = client.get(url)
    assert response.status_code == 302
    assert '/admin/login/' in response.url

    # Staff user should see the dashboard
    staff_user = User.objects.create_user(username='staff', password='password', email='staff@example.com', is_staff=True)
    client.login(username='staff', password='password')
    response = client.get(url)
    assert response.status_code == 200
    assert 'total_tournaments' in response.context
