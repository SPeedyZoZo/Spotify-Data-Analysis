import pandas as pd
import networkx as nx
from scipy.stats import pearsonr

# Load the dataset
df = pd.read_csv('song_data_smaller.csv')

# Assuming the columns are named 'Song1', 'Song2', and 'Danceability'
# Create a graph from the dataframe
G = nx.from_pandas_edgelist(df, source='Song1', target='Song2')

# Calculate average degree
average_degree = sum(dict(G.degree()).values()) / G.number_of_nodes()

# Calculate the average clustering coefficient
average_clustering = nx.average_clustering(G)

# Calculate the average shortest path length
# Note: This calculation can be very computationally expensive for large networks
# and is not possible if the graph is not connected (i.e., if there are isolated nodes)
if nx.is_connected(G):
    average_path_length = nx.average_shortest_path_length(G)
else:
    average_path_length = None

# Correlation with danceability
# Assume each node has an attribute 'Danceability' associated with it
# which is also the name of the column in the dataframe containing danceability scores
# Here we take the degree of each node and its danceability score to calculate correlation
degrees = dict(G.degree())
danceability_scores = nx.get_node_attributes(G, 'Danceability')

# Filter nodes present in both degrees and danceability scores
common_nodes = set(degrees).intersection(danceability_scores)
degree_values = [degrees[node] for node in common_nodes]
danceability_values = [danceability_scores[node] for node in common_nodes]

# Calculate Pearson correlation coefficient
correlation_coefficient, p_value = pearsonr(degree_values, danceability_values)

# Print the results
print(f'Average Degree: {average_degree}')
print(f'Average Clustering Coefficient: {average_clustering}')
print(f'Average Path Length: {average_path_length}')
print(f'Correlation between Degree and Danceability: {correlation_coefficient} (p-value: {p_value})')
