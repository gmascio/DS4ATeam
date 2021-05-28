from typing import Optional, Dict

import bs4
import requests
import re


def get_song(name: str) -> Optional[Dict]:
    lyrics = get_song_lyricsapi(name)
    if lyrics is not None:
        return lyrics

    lyrics = get_song_geniusapi(name)
    if lyrics is not None:
        return lyrics

    return None


def get_song_lyricsapi(song: str) -> Optional[Dict]:
    # Constructing request_url
    base_url = 'https://www.stands4.com/services/v2/lyrics.php?'
    uid = '8890'
    tokenid = '6MQLtdYB62diOXDC'
    format = 'json'
    term = format_song_name(song)
    request_url = f'{base_url}uid={uid}&tokenid={tokenid}&term={term}&format={format}'

    if len(song) == 0:
        return None

    song_link = requests.get(request_url)

    if song_link.status_code != 200:
        return None

    song_link = song_link.json()['result'][0]['song-link']
    webpage = requests.get(song_link).text
    bs = bs4.BeautifulSoup(webpage, features='lxml')
    lyrics = bs.pre.get_text()

    #must get song name instead of using input here
    response = {
        'song_name': song,
        'lyrics': lyrics
    }

    return response


def get_song_geniusapi(song: str) -> Optional[Dict]:
    client_access_token = '-T8dLD3Yh4rBKs2zlHF7I7iy3zHaddyte_Qe_eDB53MK3-LrgOfDUq5xub5mwMUw'
    base_url = "http://api.genius.com/search?q="
    headers = {'Authorization': f'Bearer {client_access_token}'}
    search_term = format_song_name(song)
    search_url = f'{base_url}{search_term}'

    if len(song) == 0:
        return None

    response = requests.get(search_url, headers=headers)
    response_json = response.json()
    path = response_json['response']['hits'][0]['result']['api_path']


    page_url = "http://genius.com" + path
    webpage = requests.get(page_url)


    bs = bs4.BeautifulSoup(webpage.text, 'html.parser')
    [h.extract() for h in bs(['script'])]
    regex = re.compile("Lyrics__Container*")
    lyrics = bs.body.find('div', class_=regex).get_text(separator=' ').strip()

    response = {
        'song_name': song,
        'lyrics': lyrics
    }
    return response


def format_song_name(string: str) -> str:
    if len(string) > 0:
        return string.replace(" ", "%20")
    return None

get_song_geniusapi('Never Gonna Give You Up')