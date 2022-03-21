import subprocess
from pathlib import Path

from .args import WEBP_QUALITY, IMAGE_DELETE, WEBP_COMMAND, DRY_RUN


def convert_image(path: Path = None):
    f = path
    code = 0
    if not f.with_suffix(".webp").exists():
        args = [
            WEBP_COMMAND,
            f'{f.resolve()}',
            '-quality', WEBP_QUALITY,
            f'{f.with_suffix(".webp").resolve()}'
        ]
        print(' '.join(['IMAGE:', *args]))
        p = subprocess.run(args)
        code = p.returncode
    if IMAGE_DELETE and code == 0:
        print(f'Deleting file: {f.resolve()}')
        if not DRY_RUN:
            f.unlink()
