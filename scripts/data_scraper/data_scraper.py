import os

# from config import *
import pandas as pd

CURR_DIR = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")
PROJECT_ROOT =  os.path.dirname(CURR_DIR).replace("\\", "/")

DATA_DIR = os.path.join(PROJECT_ROOT, 'data').replace("\\", "/")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'output').replace("\\", "/")

print(CURR_DIR)

# Define articles we want to download
article1 = "Taylor_Swift"
article2 = "Kanye_West"

# Create necessary directories if they don't exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(os.path.join(DATA_DIR, "DataFrames"), exist_ok=True)

# # Download revisions for both articles
# print("Downloading revisions for first article...")
# os.system(f'python scripts/data_scraper/download_wiki_revisions.py "{article1}"')
# print("\nDownloading revisions for second article...")
# os.system(f'python scripts/data_scraper/download_wiki_revisions.py "{article2}"')

# Convert all downloaded revisions to DataFrames
print("\nConverting revisions to DataFrames...")
os.system(f"python scripts/data_scraper/xml_to_dataframe.py --include-text")

# Load and verify one of the DataFrames
print("\nVerifying DataFrame contents...")
df = pd.read_feather(f"{DATA_DIR}/DataFrames/{article1}.feather")

# Display basic information about the DataFrame
print("\nDataFrame Info:")
print(df.info())

print("\nFirst few rows:")
print(df.head())

# Display some basic statistics
print("\nBasic statistics:")
print(f"Total number of revisions: {len(df)}")
print(f"Date range: from {df['timestamp'].min()} to {df['timestamp'].max()}")
print(f"Number of unique editors: {df['username'].nunique()}")