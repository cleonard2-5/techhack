from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .spotify_utils import get_random_song_from_playlist

# Create your views here.
def index(request, lobby_id):
    return render(request, 'lobby/index.html', {'lobby_id': lobby_id})

@login_required
def game(request):
    mode = request.GET.get('mode', 'genre')
    rounds = request.GET.get('rounds', '5')
    detail = request.GET.get('detail', 'none')
    lobby_id = request.GET.get('lobby_id', 'unknown')

    # Default empty variables
    song_url = ""
    song_cover = ""
    song_name = ""
    song_artist = ""

    # Fetch a song if it's a Spotify playlist!
    if mode == 'spotify':
        song_data = get_random_song_from_playlist(detail)
        if song_data:
            song_url = song_data['preview_url']
            song_cover = song_data['cover_art']
            song_name = song_data['name']
            song_artist = song_data['artist']

    context = {
        'mode': mode,
        'rounds': rounds,
        'detail': detail,
        'lobby_id': lobby_id,
        
        # Pass the song variables to the HTML
        'song_url': song_url,
        'song_cover': song_cover,
        'song_name': song_name,
        'song_artist': song_artist,
    }
    
    return render(request, 'lobby/game.html', context)

def results(request):
    return render(request, 'lobby/results.html')
