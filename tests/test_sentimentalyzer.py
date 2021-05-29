from unittest import mock
from unittest.mock import MagicMock

from lyrics_api import get_song, get_song_lyricsapi, format_song_name, get_song_geniusapi
import requests_mock

from sentimentalyzer import remove_words_in_brackets, lyric_sentimentalyzer, sentimentalyzer, word_sentiment


def test_sentimentalyzer():
    assert type(sentimentalyzer('yessir')) == float
    assert sentimentalyzer('yessir') == 0.0
    assert sentimentalyzer('Love') == 0.6369
    assert sentimentalyzer('Hate') == -0.5719


def test_lyric_sentimentalyzer():
    lyrics = "[Intro] Oooooh we're halfway there. Ooooh Living on a prayer. [interlude] Living on a prayer"
    response = lyric_sentimentalyzer(lyrics)
    assert type(response['entire_thing']) == float
    assert len(response['words']) > 0
    assert type(response['words']) == list

def test_word_sentiment():
    lyrics = "Oooooh we're halfway there. love Living on a prayer. Living on a prayer"
    response = word_sentiment(lyrics)
    assert type(response) == list
    assert len(response) == 13
    assert response[4] == 'love: 0.6369'


def test_remove_words_in_brackets():
    assert remove_words_in_brackets('') == ''
    assert remove_words_in_brackets('no brackets') == 'no brackets'
    assert remove_words_in_brackets('bracket in [the] middle') == 'bracket in middle'
    assert remove_words_in_brackets('[starts] with a bracket') == 'with a bracket'
    assert remove_words_in_brackets('ends with a [bracket]') == 'ends with a'
    assert remove_words_in_brackets('[nothing but bracket]') == ''