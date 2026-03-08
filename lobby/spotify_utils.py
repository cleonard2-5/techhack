import os
import random
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

load_dotenv()

def get_random_song_from_playlist(playlist_url):
    try:
        client_credentials_manager = SpotifyClientCredentials(
            client_id=os.environ.get('SPOTIPY_CLIENT_ID'),
            client_secret=os.environ.get('SPOTIPY_CLIENT_SECRET')
        )
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

        # 1. Safely extract the ID
        if 'playlist/' in playlist_url:
            playlist_id = playlist_url.split('playlist/')[1].split('?')[0]
        else:
            playlist_id = playlist_url.split('/')[-1].split('?')[0]

        # 2. Try to fetch the playlist
        try:
            results = sp.playlist_tracks(playlist_id)
        except Exception as e:
            print(f"Spotify API Error: {e}")
            return {"error": "Invalid link! Make sure it is a public 'open.spotify.com/playlist/...' link."}

        tracks = results.get('items', [])
        
        # 3. Filter for playable tracks
        valid_tracks = []
        for item in tracks:
            track = item.get('track')
            if track and track.get('preview_url'):
                valid_tracks.append(track)

        if not valid_tracks:
            return {"error": "Spotify blocked the previews for EVERY song in this playlist! Try an indie or older playlist."}

        # 4. Success! Pick a track
        random_track = random.choice(valid_tracks)

        return {
            'name': random_track['name'],
            'artist': random_track['artists'][0]['name'],
            'preview_url': random_track['preview_url'], 
            'cover_art': random_track['album']['images'][0]['url'] if random_track['album']['images'] else None
        }

    except Exception as e:
        print(f"Server Fetch Error: {e}")
        return {"error": f"Server Error: {str(e)}"}
    
def get_random_song_by_artist(artist_name):
    try:
        client_credentials_manager = SpotifyClientCredentials(
            client_id=os.environ.get('SPOTIPY_CLIENT_ID'),
            client_secret=os.environ.get('SPOTIPY_CLIENT_SECRET')
        )
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

        # 1. Search for the artist
        result = sp.search(q=f"artist:{artist_name}", type='artist', limit=1)
        if not result['artists']['items']:
            return None
        
        artist_id = result['artists']['items'][0]['id']

        # 2. Get their top tracks
        top_tracks = sp.artist_top_tracks(artist_id)['tracks']

        # 3. Filter for tracks WITH an audio clip
        valid_tracks = [track for track in top_tracks if track.get('preview_url')]

        if not valid_tracks:
            return None

        # 4. Pick a random valid track
        random_track = random.choice(valid_tracks)

        return {
            'name': random_track['name'],
            'artist': random_track['artists'][0]['name'],
            'preview_url': random_track['preview_url'], 
            'cover_art': random_track['album']['images'][0]['url'] if random_track['album']['images'] else None
        }
    except Exception as e:
        print(f"Spotify Artist Fetch Error: {e}")
        return None


def get_random_song_by_genre(genre_name):
    try:
        client_credentials_manager = SpotifyClientCredentials(
            client_id=os.environ.get('SPOTIPY_CLIENT_ID'),
            client_secret=os.environ.get('SPOTIPY_CLIENT_SECRET')
        )
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

        # For broad searches like genres, a While Loop is useful to keep fetching 
        # random offsets until we find a song with a preview URL
        max_attempts = 10
        attempts = 0

        while attempts < max_attempts:
            # Pick a random offset to get truly random songs in the genre
            random_offset = random.randint(0, 500)
            results = sp.search(q=f"genre:{genre_name}", type='track', limit=10, offset=random_offset)
            tracks = results['tracks']['items']

            # Check if any of these 10 tracks have a preview_url
            valid_tracks = [track for track in tracks if track.get('preview_url')]
            
            if valid_tracks:
                random_track = random.choice(valid_tracks)
                return {
                    'name': random_track['name'],
                    'artist': random_track['artists'][0]['name'],
                    'preview_url': random_track['preview_url'], 
                    'cover_art': random_track['album']['images'][0]['url'] if random_track['album']['images'] else None
                }
            
            attempts += 1 # Try again if none of the 10 had audio clips

        return None # Gave up after 10 attempts
    except Exception as e:
        print(f"Spotify Genre Fetch Error: {e}")
        return None