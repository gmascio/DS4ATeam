from unittest import mock
from unittest.mock import MagicMock

from lyrics_api import get_song, get_song_lyricsapi, format_song_name, get_song_geniusapi
import requests_mock

from sentimentalyzer import remove_words_in_brackets, lyric_sentimentalyzer


def test_sentimentalyzer():
    return None


def test_lyric_sentimentalyzer():
    lyrics = "[Intro] Oooooh we're halfway there. Ooooh Living on a prayer. [interlude] Living on a prayer"
    assert lyric_sentimentalyzer(lyrics) == int
    return None


def test_remove_words_in_brackets():
    assert remove_words_in_brackets('') == ''
    assert remove_words_in_brackets('no brackets') == 'no brackets'
    assert remove_words_in_brackets('bracket in [the] middle') == 'bracket in middle'
    assert remove_words_in_brackets('[starts] with a bracket') == 'with a bracket'
    assert remove_words_in_brackets('ends with a [bracket]') == 'ends with a'
    assert remove_words_in_brackets('[nothing but bracket]') == ''