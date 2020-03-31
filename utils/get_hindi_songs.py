# Importing required libraries
from bs4 import BeautifulSoup as bs
import requests
import argparse
import logging
import datetime

from storage.storage_class import Songs

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s:  %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# Declaring variables for collecting info
HOST = "http://myswar.co/{}"

DEFAULT_OUT_DIR = '/tmp/'
DEFAULT_FILE_NAME = 'test.csv'


# Function to get URL for albums of the year
def _get_year_url(year):
    year_string = "album/year/{}"
    url_for_year = HOST.format(year_string.format(year))
    return (url_for_year)


# Function to get total pages for an year
def _get_total_pages(year):
    url_for_year = _get_year_url(year)
    response = requests.get(url_for_year)
    attrs = {
        'title': 'Go to last page'
    }
    parsed_page = bs(response.content, 'html5lib')
    total_pages_link = parsed_page.find('a', attrs=attrs)['href']
    total_pages = total_pages_link.split('?')[0].split('year/')[1] \
        .split('/')[1]
    return int(total_pages)


def _get_album_from_table(album_table):
    name = album_table.tbody.tr.td.a['title']
    link = album_table.tbody.tr.td.a['href']
    return [name, link]


def _get_albums_for_a_page(year, page):
    url_for_year = _get_year_url(year)
    url_for_page = url_for_year + "/{}".format(page)
    all_albums = []
    response = requests.get(url_for_page)
    div_attrs = {
        'class': 'albumlisting_width'
    }
    table_attrs = {
        'class': 'song_detail_display_table'
    }
    parsed_page = bs(response.content, 'html5lib')
    albums_div = parsed_page.find('div', attrs=div_attrs)
    all_albums_tables = albums_div.findAll('table', attrs=table_attrs)
    for album_table in all_albums_tables:
        all_albums.append(_get_album_from_table(album_table))
    return (all_albums)


def _get_songs_from_albums(album_list, songs_store, year):
    total_processed = 0
    for album in album_list:
        attrs = {
            'class': 'song_detail_display_table'
        }
        response = requests.get(album[1])
        parsed_page = bs(response.content, 'html5lib')
        songs_tables = parsed_page.findAll('table', attrs=attrs)
        for song_table in songs_tables:
            lst_songs = _get_songs_details_from_table(song_table)
            total_processed = _process_song(
                lst_songs,
                songs_store,
                album[0],
                year
            )
    return total_processed
            


def _get_songs_details_from_table(song_table):
    list_tr = song_table.tbody.findAll('tr')
    list_returned = _get_name_and_download_link(list_tr[0])
    if list_returned:
        song_name = list_returned[0]
        download_link = list_returned[1]
    else:
        song_name = None
        download_link = None
    list_returned = _get_song_meta(list_tr[2])
    if list_returned:
        singers = list_returned[0]
        directors = list_returned[1]
    else:
        singers = None
        directors = None
    if song_name and download_link and singers and directors:
        return [song_name, download_link, singers, directors]
    else:
        pass


def _get_name_and_download_link(table):
    song_name = table.find('td', attrs={
                'colspan': '2'
            }).a['title']
    try:
        download_link = table.find('td', attrs={
            'rowspan': '2'
        }).table.tbody.tr.findAll('td')[1].a['href']
        if "youtube" not in download_link:
            download_link = None
            return None
        return [song_name, download_link]
    except:
        return None


def _get_song_meta(table):
    try:
        required_td = table.findAll('td')[0]
        singers = []
        directors = []
        tr_1 = required_td.table.tbody.findAll('tr')[0]
        tr_2 = required_td.table.tbody.findAll('tr')[1]
        for span in tr_1.td.findAll('span'):
            if span.text == "Singer:":
                continue
            else:
                for singer in span.findAll('a'):
                    singers.append(singer.text)
        for span in tr_2.td.findAll('span'):
            if span.text == "Music Director:":
                continue
            else:
                for director in span.findAll('a'):
                    directors.append(director.text)
        return [singers, directors]
    except:
        return None


def _process_song(song_details, songs_storage, album_name, year):
    if song_details:
        total = songs_storage.add_item(
            title=song_details[0],
            singers = song_details[2],
            album=album_name,
            year=year,
            download_link = song_details[1],
            directors = song_details[3]
        )
        return total
    else:
        return 0


def main(year, output_dir=DEFAULT_OUT_DIR, file_name=DEFAULT_FILE_NAME):
    logger.info("Started for year{}".format(year))
    songs_storage = Songs(
        year,
        output_dir,
        file_name
    )
    total_pages = _get_total_pages(year)
    for page in range(1, total_pages+1):
        albums_of_page = _get_albums_for_a_page(
            year,
            page
        )
        processed_songs = _get_songs_from_albums(
            albums_of_page,
            songs_storage,
            year
        )
        if processed_songs != 0:
            logger.info("Total songs processed for page{} : {}".format(page, processed_songs))
    total_songs_added = songs_storage.commit()
    logger.info("Total Songs Written to disk : {}".format(total_songs_added))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Get Hindi songs',
        add_help=True,
    )
    parser.add_argument(
        '--year',
        help='Get data for an year.')
    parser.add_argument(
        '--dir',
        help='Specify output directory')
    parser.add_argument(
        '--file',
        help='Specify file name')
    args = parser.parse_args()
    if args.year:
        year = args.year
    else:
        year = datetime.datetime.now.year()
    if args.dir:
        output_dir = args.dir
    else:
        output_dir = DEFAULT_OUT_DIR
    if args.file:
        output_file = args.file
    else:
        output_file = DEFAULT_FILE_NAME       

    main(year, output_dir, output_file)
