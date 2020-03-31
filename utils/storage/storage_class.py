import logging
from collections import namedtuple
import csv
import os

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

_LIST_OF_INFO = [
    'title',
    'singers',
    'album',
    'download_link',
    'directors',
    'year',
    'film',
    'cast',
]

_SONG_CLASS = namedtuple(
    'Song',
    [i for i in _LIST_OF_INFO]
)


class Songs:

    def __init__(
        self,
        year,
        output_dir=None,
        output_file=None,
        buffer_length = 100,
    ):
        self._OUTPUT_DIR = output_dir
        self._YEAR = year
        self._OUTPUT_FILE = output_file
        self._total_sounds = 0
        self._songs_buffer = []
        self._BUFFER_LENGTH = buffer_length

        if not os.path.exists(self.create_output_path(
            output_dir, output_file
        )):
           with open(
                self.create_output_path(
                    self._OUTPUT_DIR,
                    self._OUTPUT_FILE),
                    'w',
                    newline=''
            ) as file:
                writer = csv.writer(file)
                writer.writerow([
                    'title',
                    'singers',
                    'album',
                    'download_link',
                    'directors',
                    'year',
                    'film',
                    'cast'
                ])

        logging.info("Initialized with year {}".format(self._YEAR))

    def add_item(
        self,
        title,
        singers,
        album,
        download_link,
        directors,
        year,
        film=None,
        cast=None
    ):
        song = _SONG_CLASS(
            title=title,
            singers=singers,
            album=album,
            download_link = download_link,
            directors=directors,
            year=year,
            film=film,
            cast=cast
        )
        song_row = self._create_csv_row(song)

        if song_row:
            self._songs_buffer.append(song_row)
            self._total_sounds += 1
        if len(self._songs_buffer) >= self._BUFFER_LENGTH:
            self._flush_buffer()

        return self._total_sounds

    def _create_csv_row(
        self,
        song,
        parameters = _LIST_OF_INFO
    ):
        row = []
        try:
            for value in song:
                row.append(value)

        except:
            logging.warning("Some parameter is missing")
        return row

    def _flush_buffer(self):
        buffer_length = len(self._songs_buffer)
        if buffer_length > 0:
            logging.info(
                'Writing {} lines from buffer to disk.'
                .format(buffer_length)
            )
            with open(
                self.create_output_path(
                    self._OUTPUT_DIR,
                    self._OUTPUT_FILE),
                    'a',
                    newline=''
            ) as file:
                writer = csv.writer(file)
                writer.writerows([row for row in self._songs_buffer])
            self._songs_buffer = []

    def create_output_path(
        self,
        output_dir,
        output_file
    ):
        return os.path.join(output_dir, output_file)

    def commit(self):
        self._flush_buffer()
        return self._total_sounds
