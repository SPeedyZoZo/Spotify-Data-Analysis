# Spotify Digital Media and Social Networks Coursework Group Project Code

## License

This project is released under the MIT License, which permits free use, modification, and distribution of the software.

## Take Down Request

If there are any concerns regarding the content of this repository, such as copyright issues or requests for removal by course administrators or others, please contact me directly. I am committed to addressing such concerns promptly and will remove the content if necessary.

## Acknowledgements

This project was supervised by the faculty of Queen Mary University of London and is submitted as part of the academic requirements of the Digital Media and Social Networks module. The application serves as an educational tool to understand and apply basic as well as advanced data analysis techniques in a practical setting.

This repository's code was **NOT** submitted as part of our project, but the graphs, data and analyses we extracted from the code were submitted and graded.

## Note on Example Data

The repository includes several example datasets (`interactions_bigger.csv`, `song_data_smaller.csv`, etc.), stored in various file formats to demonstrate the compatibility and functionality of the data analysis operations within this application.

###### Disclaimer: Please note that this repository may appear messy as it includes experimental code that was not graded or marked. The code provided by QMUL as boilerplate is also included, although now drastically different to what they provided. However, the remaining code was written by me and is relevant to the project.

## Files Description

### Python Scripts:
- `analysisData.py`: Demonstrates the application of pandas for data manipulation and networkx for graph analysis. It reads data from a CSV file named `song_data_smaller.csv`, constructing a graph from this data to identify patterns or clusters within music data.
- `attributeGet.py`: Uses the Spotipy library to fetch data about Spotify tracks or artists, setting up Spotify client credentials and demonstrating methods to retrieve and possibly store track attributes.
- `old_spotify.py`: Analyzes artist popularity within a Spotify playlist, fetching data from the Spotify API, categorizing artists by popularity, and performing statistical analysis.
- `otherdetails.py`: Manages Spotify API authentication and might include functions for fetching and processing specific Spotify data using requests for HTTP calls.
- `spotify.py`: Intended as a script for a new Spotify playlist management feature, outlines essential components for handling Spotify data, was incomplete.
- `tutorial.py`: Serves as an educational tool demonstrating the application of pandas and networkx in a music data context, including data visualisation and basic network statistics. This was our initial boilerplate code provided by QMUL, which has since been expanded upon and altered.

### Notebooks:
- `a.ipynb`: A Jupyter notebook that serves as a platform for exploratory data analysis, prototyping Spotify API interactions, or visualizing music data analytics.

### Data Files:
#### CSV Files:
- `enriched_song_data copy 2.csv` & `enriched_song_data.csv`: Contains enriched song data with extended attributes for in-depth analysis.
- `interactions_bigger.csv` & `interactions_smaller.csv`: Contains user interaction data with songs or playlists, useful for analyzing user behavior.
- `playlist_data_bigger.csv` & `playlist_data_smaller.csv`: Includes data on playlists with details such as names and track counts, useful for analyzing playlist popularity and user engagement.
- `song_data_bigger.csv` & `song_data_smaller.csv`: Includes song metadata, supporting various uses from testing algorithms to detailed analytics.

#### Text Files:
- `SpotifyCodes.txt`: Contains API credentials and access tokens, essential for interacting with the Spotify API. Lists several playlists by ID and track count, providing a ready dataset for API interaction examples or testing.

## Prerequisites

Before you begin using this application, ensure you have the following installed:
- Python 3.8 or higher
- Required Python packages: `pandas`, `networkx`, `spotipy`, `requests` and more (installation instructions can be found in the requirements.txt file).

## Installation

To set up this project for local development and testing:
1. Clone the repository to your local machine.
2. Install the required dependencies:
  ```
  pip install -r requirements.txt
  ```

## Usage

To use this application:
1. First, obtain your Spotify API credentials (Client ID and Client Secret) and fill them in where required in the scripts.
2. Run the individual scripts to perform tasks like data fetching, analysis, or simulation of interactions. For example:
  ```
  python attributeGet.py
  ```
3. Use the Jupyter notebook (a.ipynb) for interactive data analysis and visualization.

## Contributions and Plagarism

Please note that this repository is for showcasing our work and is not intended for contributions or plagiarism. If this repository becomes private, any further access will require our permission.

## Issues

If you encounter any problems or have feedback, please open an issue on this repository, detailing the problem and how to reproduce it (no guarantees it will be fixed as this repository is just a showcase of our work submission). 


## Final Thoughts

This README provides a comprehensive guide to help you get started with our Spotify API Data Analysis application. I hope you find this project useful for learning and applying data science techniques to real-world music data. 
