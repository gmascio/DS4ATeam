import csv
import os
from pandas import read_csv
from lyrics_api import get_song
import pandas as pd


# CSV File location below must include columns ('song_name' & 'artist_name')
with open('UMG_Raw_Song_Data.csv', encoding='utf-8') as f:
    spotify_data = read_csv(f, encoding="utf-8", delimiter=',')

spotify_data = spotify_data.dropna(subset=['artist_name'])

# Creating new DF with just 'song_name' & 'artist_name'
song_data = pd.DataFrame()
song_data['song_name'] = spotify_data['song_name']
song_data['artist_name'] = spotify_data['artist_name']

# Dropping duplicates to avoid pulling the same song twice.
song_data = song_data.drop_duplicates()
song_data = song_data.drop_duplicates(subset=['song_name'])

# Output will be saved to the below filename.
output_path = 'song_lyric_data.csv'

# Looping through each row in the song_data Dataframe to try to get_song.
# song_name, lyrics, artist are pushed to the filename above.
for i, row in song_data.iterrows():
    song_lyrics = get_song(str(row.song_name), str(row.artist_name))

    if song_lyrics is not None:

        song_name = song_lyrics['song_name']
        lyrics = song_lyrics['lyrics']
        artist = song_lyrics['artist']

        print(f'{song_name} by {artist} | lyrics: {lyrics}')

        df = pd.DataFrame({'song_name': song_name, 'lyrics': lyrics, 'artist': artist}, index=[i])
        df.to_csv(output_path, mode='a', header=not os.path.exists(output_path))
        print(f'({i}) Pushed song {str(row.song_name)} by {str(row.artist_name)}')

    else:

        df = pd.DataFrame({'song_name': "None", 'lyrics': "None", 'artist': "None"}, index=[i])
        df.to_csv(output_path, mode='a', header=not os.path.exists(output_path))
        print(f'({i}) Song not found. Pushed "None"')
