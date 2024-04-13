# import pandas as pd
# import networkx as nx
# import matplotlib.pyplot as plt


# # Load
# G = pd.read_pickle("smaller_graph.pickle")


# # Calc basic measures
# nodes = G.number_of_nodes()
# edges = G.number_of_edges()
# AVGdegree = sum(dict(G.degree()).values()) / nodes # make dictionary from degree of each node, and then calc average with sum of all degrees / sum of all nodes


# # Centrality measures
# degreeCentrality = nx.degree_centrality(G) #
# average_degree_centrality = sum(degreeCentrality.values()) / nodes


# #
# betweennessCentrality = nx.betweenness_centrality(G)
# average_betwenness_centrality = sum(betweennessCentrality.values()) / nodes
   
# #
# closenessCentrality = nx.closeness_centrality(G)
# average_closeness_centrality = sum(closenessCentrality.values()) / nodes


# #
# eigenvectorCentrality = nx.eigenvector_centrality(G, max_iter=500)
# average_eigenvector_centrality = sum(eigenvectorCentrality.values()) / nodes


# print("Average degree:", AVGdegree)
# print("Degree Centrality:", average_degree_centrality)
# print("Betweenness Centrality:", average_betwenness_centrality)
# print("Closeness Centrality:", average_closeness_centrality)
# print("Eigenvector Centrality:", average_eigenvector_centrality)
# print("Nodes:", nodes)
# print("Edges:", edges)


# # Calc node size based on centrality
# sizes = [degreeCentrality[node] * 1000 for node in G.nodes()]


# # Plot
# plt.figure(figsize=(10, 8))
# plt.title("Co-occurrence of Songs Including Node Size by Influence (1-B)")
# nx.draw(G, pos=nx.kamada_kawai_layout(G), with_labels=False, node_size=sizes, font_size=5, alpha=0.7, width=0.2)
# plt.show()

############################


# # the song data is stored in a csv file called song_data_bigger.csv formatted like this:
# # song_id,song_name,artist_name,artist_uri,album_name,album_uri
# # I want to use the spotify api to investigate the following API data based on our large dataset of song data (mainly using song IDs).

# # Danceability describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity. A value of 0.0 is least danceable and 1.0 is most danceable.
# # The overall estimated tempo of a track in beats per minute (BPM). In musical terminology, tempo is the speed or pace of a given piece and derives directly from the average beat duration.
# # Energy is a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy. For example, death metal has high energy, while a Bach prelude scores low on the scale. Perceptual features contributing to this attribute include dynamic range, perceived loudness, timbre, onset rate, and general entropy.
# # Speechiness detects the presence of spoken words in a track. The more exclusively speech-like the recording (e.g. talk show, audio book, poetry), the closer to 1.0 the attribute value. Values above 0.66 describe tracks that are probably made entirely of spoken words. Values between 0.33 and 0.66 describe tracks that may contain both music and speech, either in sections or layered, including such cases as rap music. Values below 0.33 most likely represent music and other non-speech-like tracks.
# # The overall loudness of a track in decibels (dB). Loudness values are averaged across the entire track and are useful for comparing relative loudness of tracks. Loudness is the quality of a sound that is the primary psychological correlate of physical strength (amplitude). Values typically range between -60 and 0 db.

# import spotipy
# from spotipy.oauth2 import SpotifyClientCredentials
# import pandas as pd
# import time

# # Initialize Spotipy client with your credentials
# client_credentials_manager = SpotifyClientCredentials(client_id='1b25813dc96f419fa85b1ac382f8ec8b', client_secret='266c03012092494789ff1ee697415226')
# sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager, requests_timeout=10, retries=10)

# # Load the dataset
# df = pd.read_csv('song_data_smaller.csv')

# # Split song IDs into batches of 100
# song_ids = df['song_id'].tolist()
# batches = [song_ids[i:i + 100] for i in range(0, len(song_ids), 100)]
# print(f"Fetching audio features for {len(song_ids)} songs in {len(batches)} batches...")
# print(song_ids)
# # Initialize an empty list to hold song attributes
# song_attributes = []

# # Function to fetch audio features for a batch of songs
# def fetch_audio_features_for_batch(song_ids_batch):
#     attempts = 0
#     while attempts < 5:
#         try:
#             return sp.audio_features(tracks=song_ids_batch)
#         except spotipy.SpotifyException as e:
#             if e.http_status == 429:
#                 wait_time = int(e.headers.get('Retry-After', 30))
#                 print(f"Rate limit exceeded. Waiting for {wait_time} seconds...")
#                 print("Number of tracks so far: ", len(song_ids_batch))
#                 print("Number of tracks analysed in total: ", len(song_ids))
#                 time.sleep(wait_time + 1)
#                 attempts += 1
#             else:
#                 raise
#         except Exception as e:
#             print(f"An error occurred: {e}")
#             return [None] * len(song_ids_batch)  # Return a list of None to match the batch size
#     print("Max retries reached for batch")
#     return [None] * len(song_ids_batch)

# # Process each batch
# for batch in batches:
#     features_list = fetch_audio_features_for_batch(batch)
#     for features, song_id in zip(features_list, batch):
#         if features:  # Check if features were found
#             attributes = {
#                 'song_id': song_id,
#                 'danceability': features['danceability'],
#             }
#             song_attributes.append(attributes)

# # Convert the list to a DataFrame
# attributes_df = pd.DataFrame(song_attributes)

# # Merge the fetched attributes with the original DataFrame
# updated_df = pd.merge(df, attributes_df, on='song_id', how='left')

# # Save the updated DataFrame to a new CSV file
# updated_df.to_csv('song_data_smaller_updated.csv', index=False)

# print("Updated dataset saved to 'song_data_smaller_updated.csv'.")

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

# Load the graph
G = pd.read_pickle("small_graph.pickle")

# Load the song data
df = pd.read_csv('enriched_song_data.csv')

# Add danceability as an attribute to the nodes
# Assuming that the 'song_id' in your dataframe matches the nodes in the graph
# and that 'danceability' is a column in your dataframe
for index, row in df.iterrows():
    if G.has_node(row['song_id']):
        G.nodes[row['song_id']]['danceability'] = row['danceability']

# Calculate basic measures
nodes = G.number_of_nodes()
edges = G.number_of_edges()
AVGdegree = sum(dict(G.degree()).values()) / nodes

# Centrality measures
degreeCentrality = nx.degree_centrality(G)
average_degree_centrality = sum(degreeCentrality.values()) / nodes

betweennessCentrality = nx.betweenness_centrality(G)
average_betwenness_centrality = sum(betweennessCentrality.values()) / nodes

closenessCentrality = nx.closeness_centrality(G)
average_closeness_centrality = sum(closenessCentrality.values()) / nodes

eigenvectorCentrality = nx.eigenvector_centrality(G, max_iter=500)
average_eigenvector_centrality = sum(eigenvectorCentrality.values()) / nodes

# Correlation with danceability
# Prepare lists for calculating correlations
danceability_values = []
degree_values = []
for node in G.nodes():
    danceability_values.append(G.nodes[node]['danceability'])
    degree_values.append(degreeCentrality[node])

# Calculate Pearson correlation coefficient
correlation_coefficient, p_value = pearsonr(degree_values, danceability_values)

# Print the results
print("Average degree:", AVGdegree)
print("Degree Centrality:", average_degree_centrality)
print("Betweenness Centrality:", average_betwenness_centrality)
print("Closeness Centrality:", average_closeness_centrality)
print("Eigenvector Centrality:", average_eigenvector_centrality)
print("Nodes:", nodes)
print("Edges:", edges)
print(f'Correlation between Degree and Danceability: {correlation_coefficient} (p-value: {p_value})')

# Calculate node size based on centrality
sizes = [degreeCentrality[node] * 1000 for node in G.nodes()]

# Plot
plt.figure(figsize=(10, 8))
plt.title("Co-occurrence of Songs Including Node Size by Influence (1-B)")
nx.draw(G, pos=nx.kamada_kawai_layout(G), with_labels=False, node_size=sizes, font_size=5, alpha=0.7, width=0.2)
plt.show()
