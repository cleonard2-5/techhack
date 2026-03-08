from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .consumers import game_state

def index(request, lobby_id):
    return render(request, 'lobby/index.html', {'lobby_id': lobby_id})

@login_required
def game(request):
    mode = request.GET.get('mode', 'genre')
    rounds = request.GET.get('rounds', '5')
    detail = request.GET.get('detail', 'none')
    lobby_id = request.GET.get('lobby_id', 'unknown')

    context = {
        'mode': mode, 'rounds': rounds, 'detail': detail,
        'lobby_id': lobby_id, 'video_id': "", 'song_cover': "", 
        'song_name': "Loading...", 'song_artist': "Please wait",
    }
    return render(request, 'lobby/game.html', context)

@login_required
def results(request, lobby_id):
    # Fetch the scores from the in-memory game_state
    state = game_state.get(lobby_id, {})
    scores = state.get('scores', {})
    
    # Sort scores: Highest to Lowest
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    
    context = {
        'lobby_id': lobby_id,
        'sorted_scores': sorted_scores
    }
    return render(request, 'lobby/results.html', context)