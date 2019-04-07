from utils.environment import env

logger = env.get_logger(__name__)


class ArtistHelper(object):
    def __init__(self, name, score=0.0):
        self.logger = env.get_logger(self.__class__.__name__)
        self.__name = name
        self.__score = score

    @property
    def name(self):
        return self.__name

    @property
    def score(self):
        return self.__score

