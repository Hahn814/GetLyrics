import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from utils.environment import env

logger = env.get_logger(context=__name__)


class Corpus(object):

    def __init__(self, corpus: str):
        self.logger = env.get_logger(context=self.__class__.__name__)
        self.__corpus = corpus
        self.__sia = SentimentIntensityAnalyzer()

    @property
    def corpus(self):
        return self.__corpus

    def get_average_sentiment_score(self):
        sent_score = 0.0
        c = 0.0

        for score in self.get_sentiment_scores():
            sent_score += score.get('compound')
            c += 1

        return float(sent_score) / float(c)

    def get_sentiment_scores(self):
        sent_text = nltk.sent_tokenize(self.corpus)
        for sentence in sent_text:
            score = self.__sia.polarity_scores(sentence)
            yield score
