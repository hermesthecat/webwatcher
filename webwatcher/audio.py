import subprocess
from pathlib import Path

from .args import AUDIO_DELETE, DRY_RUN


def convert_audio(path: Path = None, parent: Path = None):
    f = path
    code = 0
    # Only run conversion if destination file does not exist.
    if not f.with_suffix(".webm").exists():
        args = [
            'ffmpeg', '-y',
            '-i', f'{f.resolve()}',
            '-map', '0:a',
            '-c:a', 'libopus',
            '-quality', '100',
            f'{f.with_suffix(".webm").resolve()}'
        ]
        short_args = [
            'ffmpeg', '-y',
            '-i', f'{f.relative_to(parent).resolve()}',
            '-map', '0:a',
            '-c:a', 'libopus',
            '-quality', '100',
            f'{f.with_suffix(".webm").relative_to(parent).resolve()}'
        ]
        print(' '.join(['AUDIO:', *short_args]))
        if not DRY_RUN:
            p = subprocess.run(args)
            code = p.returncode

    # Copy file to source folder
    from .utils import copy_to_source
    copy_to_source(f, parent)

    # Delete image if enabled and successful conversion
    if AUDIO_DELETE and code == 0:
        print(f'Deleting file: {f.resolve()}')

        if not DRY_RUN:
            pass

            #f.unlink()
