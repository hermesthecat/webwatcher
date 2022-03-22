import argparse
from pathlib import Path
from environs import Env

env = Env()
IS_DOCKER = env.bool('IS_DOCKER', False)


def quality(arg):
    """ Type function for argparse - a float within some predefined bounds """
    try:
        f = int(arg)
    except ValueError:
        raise argparse.ArgumentTypeError("Must be an integer")
    if f < 1 or f > 100:
        raise argparse.ArgumentTypeError("Argument must be < " + str(100) + "and > " + str(1))
    return str(f)


_parser = argparse.ArgumentParser(description='Convert media to smaller web formats.', prog='webwatcher')
_parser.add_argument('--path', type=Path, dest='paths', action='append', metavar='directory', help='a patch to watch for files', default=list())
_parser.add_argument('--source-path', type=Path, action='store', metavar='directory', help='directory to place source files (should be outside all watch directories)', default='/source')
_parser.add_argument('--dry-run', action='store_true', help='Do not process any files but show output.')
_parser.add_argument('--no-keep-source', action='store_false', dest='keep_source', help='Do not keep source files.')

# Define subcommands
subparsers = _parser.add_subparsers(help='other functions', title='subcommands', dest='subcommand', metavar='{command}')

# Watch command
p_manage = subparsers.add_parser('watch', help='Watches one or more directories for new files to convert.', )
p_manage.add_argument('--all', action='store_true', help='Deletes ALL files that match an input file extension, even if the matching webp/webm is not found.')

# Clean command
p_manage = subparsers.add_parser('clean', help='Cleans up old files that may or may not have been converted yet.')
p_manage.add_argument('--all', action='store_true', help='Deletes ALL files that match an input file extension, even if the matching webp/webm is not found.')

# Convert command
p_manage = subparsers.add_parser('convert', help='Runs a one time conversion of all matching files in the specified directories.')


a_group = _parser.add_argument_group('Audio')
a_group.add_argument('--no-watch-audio', action='store_false', help='Do not watch for audio files')
a_group.add_argument('--audio-delete', action='store_true', help='Delete source audio files when finished converting')
a_group.add_argument('--audio-format', type=str, action='append', metavar='extension', help='Extra audio formats to watch for', default=list())

i_group = _parser.add_argument_group('Images')
i_group.add_argument('--no-watch-images', action='store_false', help='Do not watch for image files')
i_group.add_argument('--image-delete', action='store_true', help='Delete source image files when finished converting')
i_group.add_argument('--image-format', type=str, action='append', metavar='extension', help='Extra image formats to watch for', default=list())
i_group.add_argument('--webp-command', type=str, nargs='?', metavar='executable_path', help='command to run for ImageMagick', default='convert')
i_group.add_argument('--webp-quality', type=quality, action='store', metavar='percent', help='conversion quality for libwebp: 1 (worst) to 100 (lossless)', default='60')
i_group.add_argument('--webp-lossless', action='store_true', help='Use lossless conversion when converting to webp')

config = _parser.parse_args()

_WATCH_DIRS = env.list('WATCH_DIRS', config.paths)
if len(_WATCH_DIRS) == 0:
    _WATCH_DIRS.append(Path('/watch'))
WATCH_DIRS = [Path(f) for f in _WATCH_DIRS]
IS_WINDOWS = env.bool('IS_WINDOWS', False)
DRY_RUN = env.bool('DRY_RUN', config.dry_run)
KEEP_SOURCE = env.bool('KEEP_SOURCE', config.keep_source)
SOURCE_PATH = env.path('SOURCE_PATH', config.source_path)

WATCH_AUDIO = env.bool('WATCH_AUDIO', config.no_watch_audio)
WATCH_IMAGES = env.bool('WATCH_IMAGES', config.no_watch_images)

AUDIO_CONVERT_FORMATS = ['.mp3', '.aac', '.flac', '.wav', '.wma', '.aac', '.m4a', '.ogg', *config.audio_format]
AUDIO_DELETE = env.bool('AUDIO_DELETE', config.audio_delete)

# Image conversion settings
IMAGE_CONVERT_FORMATS = ['.png', '.jpg', '.bmp', '.jpeg', *config.image_format]
IMAGE_DELETE = env.bool('IMAGE_DELETE', config.image_delete)
WEBP_COMMAND = env.str('WEBP_COMMAND', config.webp_command)
WEBP_LOSSLESS = env.bool('WEBP_LOSSLESS', config.webp_lossless)
WEBP_QUALITY = env.str('WEBP_QUALITY', '100' if WEBP_LOSSLESS else config.webp_quality)

