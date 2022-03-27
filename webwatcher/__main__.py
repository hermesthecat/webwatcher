import signal
from time import sleep

from .args import config
from .utils import clean_existing_files, \
    convert_existing_files, get_all_files, convert_existing_file
from .watchdog import schedule_observer, get_observer
from multiprocessing.dummy import Pool as ThreadPool

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

if config.dry_run:
    print('Dry run enabled.  Will not perform any file operations but will still print output of what would be happening.')


# Only start watcher if no subcommand is specified or watch command is specified
if config.subcommand is None or config.subcommand == 'watch':
    print('Starting watcher')
    observer = schedule_observer(observer)
    observer.start()

    # New thread pool to process multiple existing files simultaneously
    pool = ThreadPool(config.workers)

    # Run new thread pool from all existing files
    results = pool.map(convert_existing_file, get_all_files())

    # Run indefinitely so watchdog can do its thing
    while True:
        sleep(1)

elif config.subcommand == 'clean':
    print('Cleaning existing files')
    clean_existing_files(get_all_files())

elif config.subcommand == 'convert':
    print('Converting existing files')
    convert_existing_files(get_all_files())
