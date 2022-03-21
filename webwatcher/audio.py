import subprocess
from pathlib import Path

from .args import AUDIO_DELETE, DRY_RUN


def convert_audio(path: Path = None):
    f = path
    code = 0
    if not f.with_suffix(".webm").exists():
        args = [
            'ffmpeg', '-y',
            '-i', f'{f.resolve()}',
            '-map', '0:a',
            '-c:a', 'libopus',
            '-quality', '100',
            f'{f.with_suffix(".webm").resolve()}'
        ]
        print(' '.join(['AUDIO:', *args]))
        p = subprocess.run(args)
        code = p.returncode
    if AUDIO_DELETE and code == 0:
        print(f'Deleting file: {f.resolve()}')
        if not DRY_RUN:
            f.unlink()
