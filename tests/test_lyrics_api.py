from unittest import mock
from unittest.mock import MagicMock

from lyrics_api import get_song, get_song_lyricsapi, format_song_name, get_song_geniusapi
import requests_mock

def test_format_song_name():
    assert format_song_name('') is None
    assert format_song_name('test') == 'test'
    assert format_song_name('test space') == 'test%20space'

def test_get_song_lyricsapi():
    assert get_song_lyricsapi('') is None
    response = get_song_lyricsapi('Never Gonna Give You Up')
    assert type(response) == dict
    assert response['song_name'] == 'Never Gonna Give You Up'
    assert len(response['lyrics']) > 0


def test_get_song_geniusapi():
    assert get_song_geniusapi('') is None
    response = get_song_geniusapi('Never Gonna Give You Up')
    assert response['song_name'] == 'Never Gonna Give You Up'
    assert len(response['lyrics']) > 0

#def test_get_song():
#    assert get_song('') is None
#    assert get_song('NeverGonnaGiveYouUp')['song_name'] == 'NeverGonnaGiveYouUp'
#    assert len(get_song('NeverGonnaGiveYouUp')['lyrics']) > 0
