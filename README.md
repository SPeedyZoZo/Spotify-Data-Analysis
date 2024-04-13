# Spotify API Stuff

## Files Description

### Python Scripts:

- **analysisData.py**
  - This script demonstrates the application of `pandas` for data manipulation and `networkx` for graph analysis. It reads data from a CSV file named 'song_data_smaller.csv', which likely contains pairwise song relationships or attributes. A graph is then created from this data, where each node could represent a song, and edges might define relationships like similarity or collaboration. This script may be used to identify patterns or clusters within music data, enabling insights into song relationships.

- **attributeGet.py**
  - Uses the Spotipy library to interface with the Spotify API, fetching data about Spotify tracks or artists. The script sets up Spotify client credentials and demonstrates a method to retrieve and possibly store track attributes like genres, popularity scores, or artist details. This script is fundamental for anyone looking to enrich their dataset with specific Spotify metadata, making it valuable for music data analysis projects.

- **old_spotify.py**
  - A comprehensive script designed for analyzing artist popularity within a Spotify playlist. It fetches artist-related data from the Spotify API, categorizes artists by popularity, and performs statistical analysis on these categories. The script could be used to understand trends in music popularity or to create features for machine learning models predicting music trends.

- **otherdetails.py**
  - Manages Spotify API authentication and might also include functions for fetching and processing specific Spotify data. The script uses `requests` for HTTP calls, suggesting additional functionality could involve retrieving detailed artist or track information from Spotify. This script is crucial for extending Spotify data integration beyond basic track details, possibly to include lesser-known or emerging artists.

- **spotify.py**
  - Intended as a script for a new Spotify playlist management feature, it outlines the structure and essential components for handling Spotify data. While the script is in the planning or developmental stage, it includes sections for data loading, API requests, and utility functions. This script serves as a blueprint for future development of features that interact extensively with the Spotify API, likely involving playlist creation, modification, and analysis.

- **tutorial.py**
  - Likely serves as an educational tool or example script demonstrating the application of `pandas` and `networkx` in a music data context. The script might include loading a graph structure from a file, calculating basic network statistics, and visualizing data. This script is perfect for beginners or intermediates looking to understand data science applications in the music industry.

### Notebooks:

- **a.ipynb**
  - A Jupyter notebook that might serve as a platform for exploratory data analysis, prototyping Spotify API interactions, or visualizing music data analytics. The specific content and flow of the notebook would provide insights into data handling, analysis techniques, and possibly the use of visual tools to represent music data trends.

### Data Files:
- **CSV Files:**
  - `enriched_song_data copy 2.csv` & `enriched_song_data.csv`: Contains enriched song data with extended attributes for in-depth analysis.
  - `interactions_bigger.csv` & `interactions_smaller.csv`: Interaction data showing user activities with songs or playlists, useful for user behavior analysis.
  - `playlist_data_bigger.csv` & `playlist_data_smaller.csv`: Data on playlists including names, track counts, and possibly user engagement metrics.
  - `song_data_bigger.csv` & `song_data_smaller.csv`: Song metadata for various uses, from testing algorithms to detailed analytics.

### Text Files:
- **SpotifyCodes.txt**
  - Essential for API access, contains credentials and a list of playlists with details for testing or direct API interaction.


## Overview

This repository contains a range of tools and scripts for engaging with the Spotify API to extract, analyze, and interact with music data comprehensively. It provides both the basics of API interaction and advanced analytics, making it a valuable resource for developers and data analysts in the music industry.

## Usage
