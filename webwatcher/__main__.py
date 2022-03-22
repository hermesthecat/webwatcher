import signal
from time import sleep

from .args import config, DRY_RUN
from .utils import clean_files, convert_files
from .watchdog import schedule_observer, get_observer


observer = get_observer()


def finish(signum, frame):
    print('\nExiting application...')
    try:
        observer.stop()
        observer.join()
    except:
        print('Error stopping observer.')
    exit(0)


signal.signal(signal.SIGTERM, finish)
signal.signal(signal.SIGINT, finish)

if DRY_RUN:
    print('Dry run enabled.  Will not perform any file operations but will still print output of what would be happening.')

# Only start watcher if no subcommand is specified or watch command is specified
if config.subcommand is None or config.subcommand == 'watch':
    print('Starting watcher')
    observer = schedule_observer(observer)
    observer.start()
    while True:
        sleep(1)

if config.subcommand == 'clean':
    clean_files()
elif config.subcommand == 'convert':
    convert_files()
