from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .models import Tournament, Match


def check_winner(board_str):
    """ Evaluates the board string and returns 'X', 'O', 'Draw', or None """
    combinations = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Horizontal
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Vertical
        (0, 4, 8), (2, 4, 6)              # Diagonal
    ]
    for a, b, c in combinations:
        if board_str[a] != '-' and board_str[a] == board_str[b] == board_str[c]:
            return board_str[a]
    if '-' not in board_str:
        return 'Draw'  # Translated from 'Empate'
    return None


def start_tournament(request):
    """ View to input names without login and start the tournament """
    if request.method == 'POST':
        # We will also update the HTML to send 'player1' instead of 'jugador1' later
        p1 = request.POST.get('player1')
        p2 = request.POST.get('player2')

        # Create the tournament
        tournament = Tournament.objects.create(player1_name=p1, player2_name=p2)

        # Create the first match (round 1) for this tournament
        match = Match.objects.create(tournament=tournament)

        return redirect('play_match', tournament_id=tournament.id, match_id=match.id)

    return render(request, 'tictactoe/setup.html')


def play_match(request, tournament_id, match_id):
    """ View for Couch Multiplayer (Same screen) """
    tournament = get_object_or_404(Tournament, id=tournament_id)
    match = get_object_or_404(Match, id=match_id)

    if request.method == 'POST':
        # If they clicked "Next Round"
        if 'next_round' in request.POST:
            new_match = Match.objects.create(tournament=tournament)
            return redirect('play_match', tournament_id=tournament.id, match_id=new_match.id)

        # If they clicked "End Tournament"
        if 'end_tournament' in request.POST:
            tournament.is_active = False
            tournament.ended_at = timezone.now()
            tournament.save()
            return redirect('start_tournament')

        # Game logic (clicked a cell)
        if match.status == 'in_progress':
            cell = request.POST.get('cell')
            if cell is not None:
                cell = int(cell)
                board_list = list(match.board)

                # If cell is empty, allow the move
                if board_list[cell] == '-':
                    board_list[cell] = match.current_turn
                    match.board = "".join(board_list)

                    winner = check_winner(match.board)
                    if winner:
                        match.status = 'completed'
                        match.winner = winner

                        # Update tournament metrics!
                        if winner == 'X':
                            tournament.score_p1 += 1
                        elif winner == 'O':
                            tournament.score_p2 += 1
                        else:
                            tournament.draws += 1
                        tournament.save()
                    else:
                        match.current_turn = 'O' if match.current_turn == 'X' else 'X'

                    match.save()

    return render(request, 'tictactoe/board.html', {'tournament': tournament, 'match': match})


@staff_member_required(login_url='/admin/login/')
def metrics_dashboard(request):
    """ Protected analytics view: Global metrics dashboard """

    # 1. General Metrics
    total_tournaments = Tournament.objects.count()
    active_tournaments = Tournament.objects.filter(is_active=True).count()
    total_matches = Match.objects.count()

    # 2. Mathematical Aggregations
    aggregates = Tournament.objects.aggregate(
        wins_p1=Sum('score_p1'),
        wins_p2=Sum('score_p2'),
        total_draws=Sum('draws')
    )

    # Null handling
    wins_x = aggregates['wins_p1'] or 0
    wins_o = aggregates['wins_p2'] or 0
    draws = aggregates['total_draws'] or 0

    # Win Rate Calculation
    total_valid_games = wins_x + wins_o + draws
    if total_valid_games > 0:
        win_rate_x = round((wins_x / total_valid_games) * 100, 1)
        win_rate_o = round((wins_o / total_valid_games) * 100, 1)
    else:
        win_rate_x = win_rate_o = 0

    # 3. Table History: Last 10 tournaments
    recent_tournaments = Tournament.objects.all().order_by('-started_at')[:10]

    # 4. Context Packaging (English keys)
    context = {
        'total_tournaments': total_tournaments,
        'active_tournaments': active_tournaments,
        'total_matches': total_matches,
        'wins_x': wins_x,
        'wins_o': wins_o,
        'draws': draws,
        'win_rate_x': win_rate_x,
        'win_rate_o': win_rate_o,
        'recent_tournaments': recent_tournaments,
    }

    return render(request, 'tictactoe/dashboard.html', context)