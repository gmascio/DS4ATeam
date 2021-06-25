from typing import Optional, Dict

import bs4
import requests
import re


def get_song(song_name: str, artist) -> Optional[Dict]:
    try:
        # lyrics = get_song_lyricsapi(song_name, artist)
        # if lyrics is not None:
        #     return lyrics

        lyrics = get_song_geniusapi(song_name, artist)
        if lyrics is not None:
            return lyrics

    except:
        return None

    return None


def get_song_lyricsapi(song: str, artist) -> Optional[Dict]:
    # Constructing request_url
    base_url = 'https://www.stands4.com/services/v2/lyrics.php?'
    uid = '8890'
    tokenid = '6MQLtdYB62diOXDC'
    format = 'json'
    term = format_song_name(song)
    request_url = f'{base_url}uid={uid}&tokenid={tokenid}&term={term}&artist={artist}&format={format}'

    if len(song) == 0:
        return None

    response = requests.get(request_url)

    if response.status_code != 200:
        return None
    print(response.json())
    song_link = response.json()
    print(song_link)
    if type(song_link) == list:
        if len(song_link) == 0:
            return None
        song_link = song_link['result'][0]['song-link']
    else:
        if len(song_link) == 0:
            return None
        song_link = song_link['result']['song-link']

    webpage = requests.get(song_link).text
    bs = bs4.BeautifulSoup(webpage, features='lxml')
    lyrics = bs.pre.get_text()

    # must get song name instead of using input here
    response = format_response(song, lyrics, artist)
    return response


def get_artist_geniusapi(dom) -> str:
    return None


def get_song_geniusapi(song: str, artist) -> Optional[Dict]:
    client_access_token = '-T8dLD3Yh4rBKs2zlHF7I7iy3zHaddyte_Qe_eDB53MK3-LrgOfDUq5xub5mwMUw'
    base_url = "http://api.genius.com/search?q="
    headers = {'Authorization': f'Bearer {client_access_token}'}
    search_term = format_song_name(song)
    search_url = f'{base_url}{search_term}'
    artist = format_artist(artist).lower()

    if len(song) == 0:
        return None

    response = requests.get(search_url, headers=headers)
    response_json = response.json()
    path = response_json['response']['hits']
    if len(path) == 0:
        return None
    else:
        path = path[0]['result']['api_path']

    page_url = "http://genius.com" + path
    webpage = requests.get(page_url)

    bs = bs4.BeautifulSoup(webpage.text, 'html.parser')

    [h.extract() for h in bs(['script'])]

    # finding lyrics

    try:
        regex = re.compile("Lyrics__Container*")
        lyrics = bs.body.find('div', class_=regex).get_text(separator=' ').strip()
        regex = re.compile("SongInfo__Credit*")
        artists = bs.body.find('div', class_=regex).get_text()
        artists = artists[10:].lower()
    except:
        return None

    # check for the artist in the artist string
    if artist in artists:
        response = format_response(song, lyrics, artist)
        return response
    else:
        return None


def format_artist(artist: str) -> str:
    artist = artist.replace(';', ',')
    artist = artist.replace('&', ',')
    artist = artist.replace('|', ',')
    artist = artist.replace(':', ',')

    str_array = artist.split(',')
    str_array[0] = str_array[0].strip()
    return str_array[0]


def format_response(song: str, lyrics, artist: str) -> dict:
    return {
        'song_name': song,
        'lyrics': lyrics,
        'artist': artist
    }


def format_song_name(string: str) -> str:
    if len(string) > 0:
        return string.replace(" ", "%20")
    return None
