#This is a script which uses the Spotify API to analyze the popularity of artists in a playlist. The script fetches data from the Spotify API, categorizes artists based on their popularity, and performs statistical analysis on artist pairs within a playlist. The script is divided into several parts:
#1. Data Extraction Functions: Functions to extract artist URIs from a playlist and generate pairs of artists.
#2. Data Analysis Functions: Functions to analyze artist pairs based on their popularity.
#3. Example Usage: Demonstrates how to use the functions with sample data.
#4. Statistical Testing: Performs a chi-square test on observed and expected counts of artist pair categories.
#The script uses the requests library to interact with the Spotify API and the scipy library for statistical testing. The script assumes that you have already obtained an access token for the Spotify API using your client credentials. You can adapt the script to work with your specific data and requirements.
#Here is the script:

import base64
import requests

# Your updated client credentials
CLIENT_ID = ' '
CLIENT_SECRET = ' '

# Function to get an access token
def get_access_token(client_id, client_secret):
    url = 'https://accounts.spotify.com/api/token'
    payload = {
        'grant_type': 'client_credentials'
    }
    # Manually constructing the header
    client_creds = f"{client_id}:{client_secret}"
    client_creds_b64 = base64.b64encode(client_creds.encode()).decode()
    headers = {
        'Authorization': f'Basic {client_creds_b64}'
    }

    response = requests.post(url, data=payload, headers=headers)
    if response.status_code != 200:
        print("Error fetching access token:", response.text)  # This will print the error message
        return None
    token = response.json().get('access_token')
    return token

# Get the access token
access_token = get_access_token(CLIENT_ID, CLIENT_SECRET)
# print(access_token)  # This will print the access token

import pandas as pd
import time

# Assuming you have read your song_data_big.csv into a DataFrame named song_data
song_data = pd.read_csv('song_data_bigger.csv') 


# Extracting unique artist URIs
unique_artist_uris = song_data['artist_uri'].unique()



def fetch_artist_popularity_and_name(access_token, artist_uri, delay=1):
    """
    Fetches the popularity and name of an artist from the Spotify API with error handling and rate limit management.

    Parameters:
    - access_token: Spotify API access token.
    - artist_uri: The Spotify URI for the artist.
    - delay: Delay between requests in seconds to manage rate limits.

    Returns:
    - A tuple containing the artist's popularity as an integer and the artist's name as a string, or None if the request fails.
    """
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


# Example usage
artist_popularity = fetch_artist_popularity_and_name(access_token, 'spotify:artist:49tQo2QULno7gxHutgccqF')
    # print(artist_popularity)

# Dictionary to store artist URI, name, and their popularity
artist_info = {}

# Iterate over a subset of unique artist URIs to test
for artist_uri in unique_artist_uris[:10]:  # Adjust based on your testing needs
    result = fetch_artist_popularity_and_name(access_token, artist_uri)
    if result is not None:
        popularity, name = result
        artist_info[artist_uri] = {'name': name, 'popularity': popularity}
    else:
        print(f"Failed to fetch data for {artist_uri}")

# Print the collected artist information
# for artist_uri, info in artist_info.items():
#     print(f"Artist URI: {artist_uri}, Name: {info['name']}, Popularity: {info['popularity']}")


import requests

def fetch_playlist_data(access_token, playlist_id):
    headers = {
        'Authorization': f'Bearer {access_token}',
    }

    response = requests.get(f'https://api.spotify.com/v1/playlists/{playlist_id}', headers=headers)

    if response.status_code != 200:
        print(f"Failed to fetch data for playlist {playlist_id}")
        return None

    return response.json()

def extract_artists(playlist_data):
    artist_uris = []

    for item in playlist_data['tracks']['items']:
        for artist in item['track']['artists']:
            artist_uris.append(artist['uri'])

    return artist_uris

from itertools import combinations
from collections import Counter

def get_artist_pairs(artist_uris):
    return list(combinations(artist_uris, 2))

def categorize_popularity(popularity):
    """Example function to categorize popularity into three buckets."""
    if popularity > 70:
        return 'high'
    elif popularity > 40:
        return 'medium'
    return 'low'

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


# # Testing the functions
# print("Popularity Metrics: Low from 0 to 40, Medium from 41 to 70, High from 71 to 100")
# print(" --- Testing the functions ---")
# playlist_id = '37i9dQZF1DXcBWIGoYBM5M'  # A playlist ID from Spotify
# playlist_data = fetch_playlist_data(access_token, playlist_id)
# artist_uris = extract_artists(playlist_data)
# artist_pairs = get_artist_pairs(artist_uris)
# analyze_artist_pairs(artist_pairs, artist_info)

# print("_"*25)
# # Explanation of the output:
# # The output shows the count of artist pairs falling into different popularity categories.
# # For example, if there are 5 pairs where the first artist has 'high' popularity and the second artist has 'medium' popularity,
# # the output will show 'Pair Categories: ('high', 'medium'), Count: 5'.
# # This information can be useful for analyzing the relationships between artists based on their popularity levels.

import pandas as pd

# Load the data
song_data = pd.read_csv('song_data_bigger.csv')
# song_id,song_name,artist_name,artist_uri,album_name,album_uri
# 2700+ rows
interactions = pd.read_csv('interactions_bigger.csv')
# playlist_id,song_id
# 10000+ rows

# Create a mapping of song_id to artist_uri
song_to_artist = dict(zip(song_data['song_id'], song_data['artist_uri']))

from itertools import combinations
from collections import Counter

# Assuming artist_info is a dictionary mapping artist URIs to a dictionary with 'name' and 'popularity'
# Example: {'spotify:artist:4NHQUGzhtTLFvgF5SZesLK': {'name': 'Tove Lo', 'popularity': 83}}

# Create a playlist to artist URIs mapping
playlist_to_artists = interactions.groupby('playlist_id')['song_id'].apply(lambda x: [song_to_artist[song_id] for song_id in x if song_id in song_to_artist]).to_dict()

def analyze_playlist_artist_pairs(playlist_to_artists, artist_info):
    pair_category_counts = Counter()

    for playlist_id, artist_uris in playlist_to_artists.items():
        # Generate all possible artist pairs within this playlist
        artist_pairs = combinations(set(artist_uris), 2)
        
        # Categorize each pair based on the popularity of the artists
        for pair in artist_pairs:
            pop1 = artist_info.get(pair[0], {}).get('popularity', 0)
            pop2 = artist_info.get(pair[1], {}).get('popularity', 0)
            cat1 = categorize_popularity(pop1)
            cat2 = categorize_popularity(pop2)
            pair_category_counts.update([(f"{cat1}-{cat2}",)])

    # Print or return the count of artist pair categories
    for pair, count in pair_category_counts.items():
        print(f"Pair Categories: {pair}, Count: {count}")
    return pair_category_counts

# You can then call analyze_playlist_artist_pairs function with your data
pair_category_counts = analyze_playlist_artist_pairs(playlist_to_artists, artist_info)

# Statistical Testing

from scipy.stats import chisquare
import numpy as np

# Updated observed counts for each category
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

# Calculate expected counts assuming uniform distribution
expected_counts = np.full(observed_counts.shape, observed_counts.sum() / len(observed_counts))

# Perform the chi-square test
chi2_stat, p_value = chisquare(observed_counts, f_exp=expected_counts)

print(f"Chi-square Statistic: {chi2_stat}, p-value: {p_value}")
