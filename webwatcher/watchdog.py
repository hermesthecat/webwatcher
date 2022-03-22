from pathlib import Path

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers.polling import PollingObserver

from .args import config, IS_WINDOWS
from .utils import process_file


def on_created(event):
    print(f"CREATED: {event.src_path}")
    process_file(Path(event.src_path))


def get_observer():
    observer = Observer()
    if IS_WINDOWS:
        print('WARNING: Using less performant observer because host is Windows.')
        observer = PollingObserver()
    return observer


def schedule_observer(observer):
    fs_handle = PatternMatchingEventHandler(
        patterns=['*'],
        ignore_patterns=None,
        ignore_directories=False,
        case_sensitive=True
    )
    fs_handle.on_created = on_created

    for p in config.paths:
        path = Path(p)
        if path.exists():
            print(f'Watching directory {path.resolve()}')
            observer.schedule(fs_handle, f'{path.resolve()}', recursive=True)
        else:
            print(f'Skipping watch directory `{path.resolve()}` because it does not exist')
    return observer

