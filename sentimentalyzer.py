from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def sentimentalyzer(text: str) -> int:
    analyzer = SentimentIntensityAnalyzer()
    score = analyzer.polarity_scores(text)['compound']

    return score

def lyric_sentimentalyzer(lyrics: str) -> int:
    return None
    #string of x length where i have a long amount of text like this

    #[interest]length of stuff like this [interesting]

def remove_words_in_brackets(input: str) -> str:

    start_position = 0
    end_position = 0
    counter = 0

    for x in input:

        if x == '[':
            start_position = input.index(x, counter)

        if x == ']':
            end_position = input.index(x, counter)

        if end_position != 0:
            if start_position == 0:
                whole_part = input[end_position+1:]
                input = whole_part.strip()
                end_position = 0


        if start_position and end_position != 0:
            first_part = input[:start_position-1]
            last_part = input[end_position+1:]
            input = first_part + last_part
            start_position = 0
            end_position = 0

        counter += 1

    return input