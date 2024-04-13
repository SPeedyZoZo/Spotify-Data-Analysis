import csv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import backoff

# Replace with your own Spotify API credentials
client_id = ' '
client_secret = ' '

# Set up Spotipy client
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Read the input CSV file
with open('song_data_smaller.csv', 'r') as infile:
    reader = csv.DictReader(infile)
    song_data = list(reader)

# Create a new list to store the enriched data
enriched_data = []

# Define a decorator to handle rate limit errors
@backoff.on_exception(backoff.expo, spotipy.exceptions.SpotifyException, max_tries=8)
def fetch_audio_features(track_id):
    audio_features = sp.audio_features(tracks=[track_id])[0]
    if not audio_features:
        return None
    # We return only the audio features
    return {
        'danceability': audio_features['danceability'],
        'energy': audio_features['energy'],
        'valence': audio_features['valence'],
        'tempo': audio_features['tempo'],
    }

@backoff.on_exception(backoff.expo, spotipy.exceptions.SpotifyException, max_tries=8)
def fetch_artist_popularity(artist_uri):
    artist_info = sp.artist(artist_uri)
    return artist_info['popularity']

# Iterate through each song and fetch its audio features and artist popularity
for song in song_data:
    track_id = song['song_id'].split(':')[-1]
    artist_uri = song['artist_uri']
    try:
        # Fetch audio features and artist popularity separately
        audio_features = fetch_audio_features(track_id)
        artist_popularity = fetch_artist_popularity(artist_uri)
        if audio_features and artist_popularity is not None:
            song.update(audio_features)
            song['artist_popularity'] = artist_popularity
            enriched_data.append(song)
        else:
            print(f"Data not found for song {song['song_name']}")
    except spotipy.exceptions.SpotifyException as e:
        print(f"Error fetching data for song {song['song_name']}: {e}")

# Write the enriched data to a new CSV file
fieldnames = ['song_id', 'song_name', 'artist_name', 'artist_uri', 'album_name', 'album_uri', 
              'danceability', 'energy', 'valence', 'tempo', 'artist_popularity']
with open('enriched_song_data.csv', 'w', newline='') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(enriched_data)

print("Enriched data has been written to 'enriched_song_data.csv'")
