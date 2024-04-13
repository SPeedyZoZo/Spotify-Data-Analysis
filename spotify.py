# Here are all the sections I will be using to create the new Spotify playlist script.
# The above code will be used to create the new script, and will not be used after the new script is written.
"""
Imports and Constants: This section will contain all the import statements and constant definitions. This includes importing necessary modules like pandas, requests, itertools, and collections, and defining constants like CLIENT_ID and CLIENT_SECRET.

Data Loading: This section will contain the code for loading the CSV data into pandas DataFrames.

Utility Functions: This section will contain the utility functions like categorize_popularity.

API Request Functions: This section will contain the functions that make API requests, like fetch_playlist_data and fetch_artist_popularity_and_name.

Data Extraction Functions: This section will contain the functions that extract data from the API responses, like extract_artists.

Data Analysis Functions: This section will contain the functions that analyze the data, like get_artist_pairs and analyze_artist_pairs.

Artist Information Collection: This section will contain the code that collects artist information by making API requests.

Main Execution: This section will contain the main execution code that uses the functions defined in the previous sections to fetch, extract, analyze, and print the data.
"""
# This will clean up the code from spotify.py but will not alter the functionality of the script.

# Imports and Constants
import base64
import requests
import pandas as pd
import time
from itertools import combinations
from collections import Counter
from scipy.stats import chisquare
import numpy as np
from scipy.stats import chisquare
import numpy as np
from itertools import combinations

CLIENT_ID = '1b25813dc96f419fa85b1ac382f8ec8b'
CLIENT_SECRET = '75db22041dec48db9cd8c6acf1828b5e'

# Data Loading
song_data = pd.read_csv('song_data_bigger.csv')
interactions = pd.read_csv('interactions_bigger.csv')

# Utility Functions
def categorize_popularity(popularity):
    if popularity > 70:
        return 'high'
    elif popularity > 40:
        return 'medium'
    return 'low'

# API Request Functions
def get_access_token(client_id, client_secret):
    url = 'https://accounts.spotify.com/api/token'
    payload = {
        'grant_type': 'client_credentials'
    }
    client_creds = f"{client_id}:{client_secret}"
    client_creds_b64 = base64.b64encode(client_creds.encode()).decode()
    headers = {
        'Authorization': f'Basic {client_creds_b64}'
    }

    response = requests.post(url, data=payload, headers=headers)
    if response.status_code != 200:
        print("Error fetching access token:", response.text)
        return None
    token = response.json().get('access_token')
    return token

def fetch_playlist_data(access_token, playlist_id):
    headers = {
        'Authorization': f'Bearer {access_token}',
    }

    response = requests.get(f'https://api.spotify.com/v1/playlists/{playlist_id}', headers=headers)

    if response.status_code != 200:
        print(f"Failed to fetch data for playlist {playlist_id}")
        return None

    return response.json()

def fetch_artist_popularity_and_name(access_token, artist_uri, delay=1):
    base_url = 'https://api.spotify.com/v1/artists/'
    artist_id = artist_uri.split(':')[-1]
    url = f"{base_url}{artist_id}"
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    while True:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            return (data.get('popularity', None), data.get('name', 'Unknown Artist'))
        elif response.status_code == 429:
            retry_after = int(response.headers.get('Retry-After', delay))
            print(f"Rate limit reached. Retrying after {retry_after} seconds.")
            time.sleep(retry_after)
        else:
            print(f"Error fetching artist data for {artist_uri}: {response.text}")
            return None
        time.sleep(delay)

# Data Extraction Functions
def extract_artists(playlist_data):
    artist_uris = []

    for item in playlist_data['tracks']['items']:
        for artist in item['track']['artists']:
            artist_uris.append(artist['uri'])

    return artist_uris

def get_artist_pairs(artist_uris):
    return list(combinations(artist_uris, 2))

# Tests for above functions
access_token = get_access_token(CLIENT_ID, CLIENT_SECRET)
playlist_data = fetch_playlist_data(access_token, '37i9dQZF1DXcBWIGoYBM5M')
artist_uris = extract_artists(playlist_data)
artist_pairs = get_artist_pairs(artist_uris)

# Data Analysis Functions
def analyze_artist_pairs(artist_pairs, artist_info):
    pair_categories = []
    for pair in artist_pairs:
        pop1 = artist_info.get(pair[0], {}).get('popularity', 0)
        pop2 = artist_info.get(pair[1], {}).get('popularity', 0)
        cat1 = categorize_popularity(pop1)
        cat2 = categorize_popularity(pop2)
        pair_categories.append((cat1, cat2))
    
    pair_category_counts = Counter(pair_categories)
    
    for pair, count in pair_category_counts.items():
        print(f"Pair Categories: {pair}, Count: {count}")
    
    return pair_category_counts

artist_pairs = get_artist_pairs(artist_uris)
artist_info = {}  # Define the artist_info variable
pair_category_counts = analyze_artist_pairs(artist_pairs, artist_info)


# Data Extraction Functions
def extract_artists(playlist_data):
    artist_uris = []

    for item in playlist_data['tracks']['items']:
        for artist in item['track']['artists']:
            artist_uris.append(artist['uri'])

    return artist_uris

# Data Analysis Functions
def get_artist_pairs(artist_uris):
    return list(combinations(artist_uris, 2))

def analyze_artist_pairs(artist_pairs, artist_info):
    pair_categories = []
    for pair in artist_pairs:
        pop1 = artist_info.get(pair[0], {}).get('popularity', 0)
        pop2 = artist_info.get(pair[1], {}).get('popularity', 0)
        cat1 = categorize_popularity(pop1)
        cat2 = categorize_popularity(pop2)
        pair_categories.append((cat1, cat2))
    
    pair_category_counts = Counter(pair_categories)
    
    for pair, count in pair_category_counts.items():
        print(f"Pair Categories: {pair}, Count: {count}")
    
    return pair_category_counts

# Artist Information Collection
access_token = get_access_token(CLIENT_ID, CLIENT_SECRET)
unique_artist_uris = song_data['artist_uri'].unique()

artist_info = {}
song_to_artist = {}  # Define the "song_to_artist" dictionary

for artist_uri in unique_artist_uris:
    result = fetch_artist_popularity_and_name(access_token, artist_uri)
    if result is not None:
        popularity, name = result
        artist_info[artist_uri] = {'name': name, 'popularity': popularity}
    else:
        print(f"Failed to fetch data for {artist_uri}")
def analyze_playlist_artist_pairs(playlist_to_artists, artist_info):
    # Function implementation goes here
    pass


# Main Execution
playlist_to_artists = interactions.groupby('playlist_id')['song_id'].apply(lambda x: [song_to_artist[song_id] for song_id in x if song_id in song_to_artist]).to_dict()

pair_category_counts = analyze_playlist_artist_pairs(playlist_to_artists, artist_info)

# Statistical Testing
observed_counts = np.array([
    117390,  # low-low
    2744,    # low-high
    2557,    # high-low
    60,      # high-high
    81,      # low-medium
    6,       # high-medium
    30,      # medium-low
    2        # medium-high
])

expected_counts = np.full(observed_counts.shape, observed_counts.sum() / len(observed_counts))

chi2_stat, p_value = chisquare(observed_counts, f_exp=expected_counts)

print(f"Chi-square Statistic: {chi2_stat}, p-value: {p_value}")

# This will be the final script that will be used to create the new Spotify playlist script.

