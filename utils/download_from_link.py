import pafy
import pandas as pd
import os
import logging

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
failed_indexes = []


def get_audio_from_link(link, filepath):
    video = pafy.new(link)
    audio = video.getbestaudio()
    os.chdir(filepath)
    audio.download()


def process_year_and_save(
        base_dir,
        path_to_save,
        year
):
    directory_path = os.path.join(base_dir, str(year))
    file_str = "song_{}.csv"
    file_path = os.path.join(directory_path, file_str.format(year))
    file_dataframe = pd.read_csv(file_path)
    total_songs_in_file = len(file_dataframe)
    path_to_save = os.path.join(path_to_save, str(year))
    for index in range(total_songs_in_file):
        row = file_dataframe.iloc[index]
        link = row.download_link
        logging.info("Downloading - {}".format(row.title))
        try:
            get_audio_from_link(link, path_to_save)
        except:
            failed_indexes.append(index)
    return failed_indexes
