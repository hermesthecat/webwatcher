import glob
from pathlib import Path

from webwatcher.args import AUDIO_CONVERT_FORMATS, IMAGE_CONVERT_FORMATS, WATCH_DIRS, DRY_RUN
from webwatcher.audio import convert_audio
from webwatcher.images import convert_image


def process_file(path: Path):
    if path.suffix in AUDIO_CONVERT_FORMATS:
        convert_audio(path)
    elif path.suffix in IMAGE_CONVERT_FORMATS:
        convert_image(path)


def clean_files():
    for d in WATCH_DIRS:
        watch_dir = Path(d)
        files = glob.glob(f'{watch_dir.resolve()}/**/*', recursive=True)
        for f in files:
            path = Path(f)
            if not path.is_file():
                continue
            converted = None
            if path.suffix in AUDIO_CONVERT_FORMATS:
                converted = path.with_suffix('.webm')
            if path.suffix in IMAGE_CONVERT_FORMATS:
                converted = path.with_suffix('.webp')

            # If the file was a supported extension
            if converted:
                print(f'Deleting file - {path.resolve()}')
                if not DRY_RUN:
                    path.unlink(missing_ok=True)

