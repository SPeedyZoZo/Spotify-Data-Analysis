import requests
from requests.auth import HTTPBasicAuth
import pandas as pd

# Spotify API credentials
CLIENT_ID = ' '
CLIENT_SECRET = ' '

def get_spotify_access_token(client_id, client_secret):
    """Authenticate with the Spotify API and return the access token."""
    auth_url = 'https://accounts.spotify.com/api/token'
    auth_response = requests.post(auth_url, auth=HTTPBasicAuth(client_id, client_secret), data={'grant_type': 'client_credentials'})
    if auth_response.status_code == 200:
        return auth_response.json()['access_token']
    else:
        raise Exception('Failed to retrieve access token')

def get_audio_features(song_ids, access_token):
    """Fetch audio features for given song IDs."""
    audio_features_url = "https://api.spotify.com/v1/audio-features"
    headers = {'Authorization': f'Bearer {access_token}'}
    params = {'ids': ','.join(song_ids)}
    response = requests.get(audio_features_url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()['audio_features']
    else:
        raise Exception(f'Failed to fetch audio features, status code: {response.status_code}')

# Obtain the access token
access_token = get_spotify_access_token(CLIENT_ID, CLIENT_SECRET)

# Example song IDs (ensure these are the ID part of Spotify Track URIs)
song_ids = ['4iV5W9uYEdYUVa79Axb7Rh', '24JygzOLM0EmRQeGtFcIcG']  # Replace with your actual song IDs

# Fetch audio features for the example song IDs
audio_features = get_audio_features(song_ids, access_token)

# Convert the list of audio features into a DataFrame
audio_features_df = pd.DataFrame(audio_features)

# Load your song data from a CSV file
song_data_df = pd.read_csv('song_data_bigger.csv')

# Ensure the 'song_id' column in your song data contains just the ID part of the Spotify URIs
# You might need to preprocess this column to match the IDs used in fetching audio features

# Merge the audio features with the song data based on song IDs
# This assumes your song_data_df has a column named 'song_id' that corresponds to the Spotify Track IDs
merged_df = pd.merge(song_data_df, audio_features_df, left_on='song_id', right_on='id')

# Now, merged_df contains your song data along with the fetched audio features
print(merged_df.head())  # Adjust as needed for your analysis

# You can now proceed with further data analysis or visualization as required for your assignment
