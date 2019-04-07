import os
import argparse
import lyricsgenius
from utils.environment import env
from utils.textutils import Corpus

logger = env.get_logger(__name__)
HEADER = ['Artist', 'Album', 'Song', 'Year', 'Lyric Count', 'Sentiment Score']


def get_arg_parser():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    filter_parser = parser.add_argument_group('Filter the results')
    filter_parser.add_argument('--author', default=None, action='append', help='The name of the author')

    out_parser = parser.add_argument_group('Output Parameters')
    out_parser.add_argument('--max_results', default=500, help='Limit the number of results to consider')
    out_parser.add_argument('--out', default='genius.csv', help='CSV results file')

    return parser


def get_args():
    arg_parser = get_arg_parser()
    args_parsed = arg_parser.parse_args()

    return args_parsed


def format_result(artist, album, song, lyric_count, year, sentiment_score):
    return {'Artist': artist, 'Album': album, 'Song': song, 'Lyric Count': lyric_count, 'Year': year, 'Sentiment Score': sentiment_score}


if __name__ == '__main__':
    args = get_args()
    author_names = args.author
    max_results = int(args.max_results)
    outfile = env.get_csv_writer(os.path.abspath(args.out), fieldnames=HEADER)
    genius = lyricsgenius.Genius("nNhT-omaJrPgrGxd4w_qHHWXXUcTdqZMnQ7v_gr5lohgHYlYlm623WgzdjDRikNv")

    if author_names:
        for author_name in author_names:
            artist = genius.search_artist(author_name, max_songs=max_results)
            logger.info("Found: {}, Limit: {}".format(len(artist.songs), max_results))

            for song in artist.songs:
                logger.info('Author: "{}", Album: "{}", Song: "{}", Lyrics: {}, Year: {}'.format(author_name, song.album, song.title, len(song.lyrics), song.year))
                corpus = Corpus(corpus=song.lyrics)
                sentiment_score = corpus.get_average_sentiment_score()
                res = format_result(artist=author_name, album=song.album, song=song.title, lyric_count=len(song.lyrics), year=song.year, sentiment_score=sentiment_score)
                outfile.writerow(res)

