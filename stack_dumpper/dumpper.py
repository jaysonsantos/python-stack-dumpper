from __future__ import print_function
import functools
import signal
import sys
import threading
import time
import traceback

lock = threading.Lock()


def call_once(function):
    @functools.wraps(function)
    def call_function(*args, **kwargs):
        with lock:
            if hasattr(function, 'called'):
                return
            try:
                return function(*args, **kwargs)
            finally:
                setattr(function, 'called', True)
    return call_function


def _dump_data():
    with lock:
        with open('/dev/stderr', 'w') as sys_err:
            if sys.version_info.major > 2:
                log = functools.partial(print, file=sys_err, flush=True)
            else:
                log = functools.partial(print, file=sys_err)
            threads = {thread.ident: thread for thread in threading.enumerate()}
            for ident, frame in sys._current_frames().items():
                log('=' * 80)
                log('Thead', threads[ident].name, ident)
                log(''.join(traceback.format_stack(frame)))
                log('=' * 80, '\n\n\n')


def dump_data(*args, **kwargs):
    threading.Thread(target=_dump_data).start()


@call_once
def setup_dumpper():
    signal.signal(signal.SIGQUIT, dump_data)


@call_once
def setup_periodic_dumpper(seconds):
    def dump_worker():
        while True:
            time.sleep(seconds)
            _dump_data()

    threading.Thread(target=dump_worker).start()
