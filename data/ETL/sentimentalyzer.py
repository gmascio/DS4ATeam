from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def sentimentalyzer(text: str) -> float:
    analyzer = SentimentIntensityAnalyzer()
    score = analyzer.polarity_scores(text)['compound']
    return float(score)


def lyric_sentimentalyzer(lyrics: str) -> dict:
    lyrics = remove_words_in_brackets(lyrics)

    words = word_sentiment(lyrics)
    entire_thing = sentimentalyzer(lyrics)
    response = {
        'words': words,
        'entire_thing': entire_thing,
    }
    return response


def phrase_sentiment(lyrics: str) -> list:
    # This is broken at the moment. I'm not sure how i'm going to grab phrases.
    # Idea1: split by /n which means i need to retain the newlines in lyrics_api()
    # Idea2: split by special character which i input. Which means i need to check for new lines in each api.

    phrases = lyrics.split('/n')
    phrase_scores = []
    for phrase in phrases:
        phrase_scores.append(f'{phrase}: {sentimentalyzer(phrase)}')
    return phrase_scores


def word_sentiment(lyrics: str) -> list:
    words = lyrics.split(' ')
    word_scores = []
    for word in words:
        word_scores.append(f'{word}: {sentimentalyzer(word)}')
    return word_scores


def remove_words_in_brackets(input_words: str) -> str:
    start_position = 0
    end_position = 0
    counter = 0

    for x in input_words:

        if x == '[':
            start_position = input_words.index(x)

        if x == ']':
            end_position = input_words.index(x)

        if end_position != 0:
            if start_position == 0:
                whole_part = input_words[end_position + 1:]
                input_words = whole_part.strip()
                end_position = 0

        if start_position and end_position != 0:
            first_part = input_words[:start_position - 1]
            last_part = input_words[end_position + 1:]
            input_words = first_part + last_part
            start_position = 0
            end_position = 0

        counter += 1

    return input_words