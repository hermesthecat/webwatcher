import subprocess
from pathlib import Path

from .args import WEBP_QUALITY, IMAGE_DELETE, WEBP_COMMAND, DRY_RUN, SOURCE_PATH, KEEP_SOURCE


def convert_image(path: Path = None, parent: Path = None):
    f = path
    code = 0
    # Only run conversion if destination file does not exist.
    if not f.with_suffix(".webp").exists():
        args = [
            WEBP_COMMAND,
            f'{f.resolve()}',
            '-quality', WEBP_QUALITY,
            f'{f.with_suffix(".webp").resolve()}'
        ]
        short_args = [
            WEBP_COMMAND,
            f'{f.relative_to(parent).resolve()}',
            '-quality', WEBP_QUALITY,
            f'{f.with_suffix(".webp").relative_to(parent).resolve()}'
        ]
        print(' '.join(['IMAGE:', *short_args]))
        if not DRY_RUN:
            p = subprocess.run(args)
            code = p.returncode

    # Copy file to source folder
    from .utils import copy_to_source
    copy_to_source(f, parent)

    # Delete image if enabled and successful conversion
    if IMAGE_DELETE and code == 0:
        print(f'Deleting file: {f.relative_to(parent).resolve()}')
        if not DRY_RUN:
            f.unlink()
