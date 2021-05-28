from unittest import mock
from unittest.mock import MagicMock

from lyrics_api import get_song, get_song_lyricsapi, format_song_name, get_song_geniusapi
import requests_mock


#def test_get_song():
#    assert get_song('') is None
#    assert get_song('NeverGonnaGiveYouUp')['song_name'] == 'NeverGonnaGiveYouUp'
#    assert len(get_song('NeverGonnaGiveYouUp')['lyrics']) > 0

@mock.patch('lyrics_api.format_string')
def test_get_song_lyricsapi(mock_format_string: MagicMock):
    expected_return = {'Idont': 'remember'}

    with requests_mock.Mocker() as m:
        m.get('https://www.stands4.com/services/v2/lyrics.php', json=expected_return, status_code=200)

        mock_format_string.return_value = "'Never%20Gonna%20Give%20You%20Up'"

        assert get_song_lyricsapi('') is None
        response = get_song_lyricsapi('Never Gonna Give You Up')
        assert type(response) == dict
        assert response['song_name'] == 'Never Gonna Give You Up'
        assert len(response['lyrics']) > 0


def test_get_song_geniusapi():
    assert get_song_geniusapi('') is None
    assert get_song_geniusapi('NeverGonnaGiveYouUp')['song_name'] == 'NeverGonnaGiveYouUp'
    assert len(get_song_geniusapi('NeverGonnaGiveYouUp')['lyrics']) > 0


def test_format_song_name():
    assert format_song_name('') is None
    assert format_song_name('test') == 'test'
    assert format_song_name('test space') == 'test%20space'



@mock.patch('totest.format_string')
def test_get_song(mock_format_string: MagicMock):
    expected_return = {'result': 'stuff'}

    with requests_mock.Mocker() as m:
        m.get('https://www.stands4.com/services/v2/lyrics.php', json=expected_return, status_code=200)

        mock_format_string.return_value = 'Never%20Gonna'

        assert get_song('Never Gonna') == expected_return

        m.get('https://www.stands4.com/services/v2/lyrics.php', json=expected_return, status_code=500)
        assert get_song('Never Gonna') is None
