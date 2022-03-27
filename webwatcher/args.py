import argparse
import os
from pathlib import Path
from environs import Env

env = Env()
IS_DOCKER = env.bool('IS_DOCKER', False)
IS_WINDOWS = env.bool('IS_WINDOWS', False)
_parser = argparse.ArgumentParser(description='Convert media to smaller web formats.', prog='webwatcher')


def quality(arg):
    """ Type function for argparse - a float within some predefined bounds """
    try:
        f = int(arg)
    except ValueError:
        raise argparse.ArgumentTypeError("Must be an integer")
    if f < 1 or f > 100:
        raise argparse.ArgumentTypeError("Argument must be < " + str(100) + "and > " + str(1))
    return str(f)


def file_extension(arg):
    """ Type function for argparse - a float within some predefined bounds """
    if str(arg).startswith('.'):
        return str(arg)
    raise argparse.ArgumentTypeError('Argument must be a file extension starting with \'.\'')


_WATCH_DIRS = env.list('WATCH_DIRS', list())
#if len(_WATCH_DIRS) == 0:
#    _WATCH_DIRS.append(Path('/watch'))
WATCH_DIRS = [Path(f) for f in _WATCH_DIRS]
DRY_RUN = env.bool('DRY_RUN', False)
COPY_SOURCE = env.bool('COPY_SOURCE', True)
SOURCE_DIR = env.path('SOURCE_DIR', '/source')
BASE_DIR = env.path('BASE_DIR', '/watch')
WORKERS = env.int('WORKERS', 8)
DELETE_MEDIA = env.bool('DELETE_MEDIA', True)

# Audio
WATCH_AUDIO = env.bool('WATCH_AUDIO', True)
DELETE_AUDIO = env.bool('DELETE_AUDIO', True)
_AUDIO_CONVERT_FORMATS = ['.mp3', '.aac', '.flac', '.wav', '.wma', '.aac', '.m4a', '.ogg']

# Image conversion settings
WATCH_IMAGES = env.bool('WATCH_IMAGES', True)
DELETE_IMAGES = env.bool('DELETE_IMAGES', True)
_IMAGE_CONVERT_FORMATS = ['.png', '.jpg', '.bmp', '.jpeg']
WEBP_COMMAND = env.str('WEBP_COMMAND', 'magick' if os.name == 'nt' else 'convert')
WEBP_LOSSLESS = env.bool('WEBP_LOSSLESS', False)
WEBP_QUALITY = env.str('WEBP_QUALITY', '100' if WEBP_LOSSLESS else '60')


# Define subcommands
subparsers = _parser.add_subparsers(help='other functions', title='subcommands', dest='subcommand', metavar='{command}')
# Watch command
p_manage = subparsers.add_parser('watch', help='Watches one or more directories for new files to convert.', )
# Clean command
p_manage = subparsers.add_parser('clean', help='Cleans up old files that may or may not have been converted yet.')
# Convert command
p_manage = subparsers.add_parser('convert', help='Runs a one time conversion of all matching files in the specified directories.')




# General args
# TODO: use /watch if nothing provided at all, figure out how to decided to exlucde base path
_parser.add_argument('--path', type=Path, dest='watch_dirs', action='append', metavar='directory', help='a patch to watch for files', default=_WATCH_DIRS)
_parser.add_argument('--dry-run', action='store_true', help='Do not process any files but show output.', default=DRY_RUN)
_parser.add_argument('--no-copy-source', action='store_false', dest='copy_source', help='Do not copy source files to source folder.', default=COPY_SOURCE)
_parser.add_argument('--windows', action='store_true', help='Is running on Windows host. (only required when running from Docker)', default=IS_WINDOWS)
_parser.add_argument('--delete-media', action='store_true', help='Delete media files when done with them.', default=DELETE_MEDIA)
_parser.add_argument('--source-dir', type=Path, action='store', metavar='directory', help='directory to place source files (should be outside all watch directories)', default=SOURCE_DIR)
_parser.add_argument('--base-dir', type=Path, action='store', metavar='directory', help='sets base watch directory (debug only)', default=BASE_DIR)
_parser.add_argument('--workers', type=int, action='store', metavar='int', help='max number of worker threads to use for simultaneous processing.', default=WORKERS)
_parser.add_argument('--all', action='store_true', help='Deletes ALL files, even if it isn\'t a media file (excluding webm/webp files)')
_parser.add_argument('--force', action='store_true', help='Deletes matching media files, even if the converted webm/webp is not found.')

# Audio args
a_group = _parser.add_argument_group('Audio')
a_group.add_argument('--no-watch-audio', action='store_false', dest='watch_audio', help='Do not watch for audio files', default=WATCH_AUDIO)
a_group.add_argument('--no-delete-audio', action='store_true', dest='keep_audio', help='Do not delete audio (used with --delete-media)', default=DELETE_AUDIO)
a_group.add_argument('--audio-format', type=file_extension, action='append', dest='audio_convert_formats', metavar='extension', help='Extra audio formats to watch for', default=_AUDIO_CONVERT_FORMATS)  # TODO


# Image args
i_group = _parser.add_argument_group('Images')
i_group.add_argument('--no-watch-images', action='store_false', help='Do not watch for image files', default=WATCH_IMAGES)
i_group.add_argument('--no-delete-images', action='store_true', dest='keep_images', help='Do not delete images (used with --delete-media)', default=DELETE_IMAGES)
i_group.add_argument('--image-format', type=file_extension, action='append', dest='image_convert_formats',metavar='extension', help='Extra image formats to watch for', default=_IMAGE_CONVERT_FORMATS)
i_group.add_argument('--webp-command', type=str, nargs='?', metavar='executable_path', help='command to run for ImageMagick', default=WEBP_COMMAND)
i_group.add_argument('--webp-quality', type=quality, action='store', metavar='percent', help='conversion quality for libwebp: 1 (worst) to 100 (lossless)', default=WEBP_QUALITY)
i_group.add_argument('--webp-lossless', action='store_true', help='Use lossless conversion when converting to webp', default=WEBP_LOSSLESS)

config = _parser.parse_args()





