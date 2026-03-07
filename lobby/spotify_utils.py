import os
import random
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def get_random_song_from_playlist(playlist_url):
    """
    Takes a Spotify playlist link, grabs all the tracks, 
    and returns the name, preview_url, and album art of a random song.
    """
    # 1. Authenticate with Spotify
    client_credentials_manager = SpotifyClientCredentials(
        client_id=os.environ.get('SPOTIPY_CLIENT_ID'),
        client_secret=os.environ.get('SPOTIPY_CLIENT_SECRET')
    )
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    try:
        # 2. Clean the URL to get just the Playlist ID
        playlist_id = playlist_url.split('/')[-1].split('?')[0]

        # 3. Fetch the playlist tracks
        results = sp.playlist_tracks(playlist_id)
        tracks = results['items']
        
        # 4. Filter out tracks that don't have a 30-second preview (some labels block them)
        valid_tracks = [item['track'] for item in tracks if item['track']['preview_url'] is not None]

        if not valid_tracks:
            return None # No playable tracks found

        # 5. Pick a random track
        random_track = random.choice(valid_tracks)

        # 6. Extract the data we need for the game
        song_data = {
            'name': random_track['name'],
            'artist': random_track['artists'][0]['name'],
            'preview_url': random_track['preview_url'], # The 30-second mp3!
            'cover_art': random_track['album']['images'][0]['url'] if random_track['album']['images'] else None
        }

        return song_data

    except Exception as e:
        print(f"Error fetching from Spotify: {e}")
        return None