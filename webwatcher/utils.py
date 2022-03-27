import glob
from pathlib import Path

from webwatcher.MediaFile import MediaFile
from webwatcher.args import config


def get_all_files():
    # Get all files from all watched dirs
    all_files = []
    for d in config.watch_dirs:
        watch_dir = Path(d)
        files = [Path(f) for f in glob.glob(f'{watch_dir.resolve()}/**/*', recursive=True) if Path(f).is_file()]
        for f in files:
            all_files.append((f, watch_dir))
    return all_files


def convert_existing_files(file_pairs):
    for path, parent in file_pairs:
        media = MediaFile(path, parent=parent)
        media.process_file()


def convert_existing_file(file_pair):
    path, parent = file_pair
    media = MediaFile(path, parent=parent)
    media.process_file()


def clean_existing_files(file_pairs):
    for path, parent in file_pairs:
        media = MediaFile(path, parent=parent)
        media.clean(copy=True)

