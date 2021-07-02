import pandas as pd

spotify_data = pd.read_csv('UMG_DATA.csv')
popularity = pd.read_csv('Spotify_Popularity.csv')
audio_features = pd.read_csv('Spotify_AudioFeatures.csv')

merged_data = spotify_data[['spotify_id', 'label_studio', 'content_provider_name', 'major_label',
                            'original_release_date',
                            'genre_name', 'isrc_weekly_streams', 'artist_name',
                            'song_name']].merge(audio_features,
                                                how='inner', left_on='spotify_id', right_on='id').drop('id', axis=1)

final_merged_data = merged_data.merge(popularity[['spotify_id', 'spotify_popularity']], how='inner', on='spotify_id')

final_merged_data.to_csv('final_merged_data.csv', encoding='utf-8', index=False)
