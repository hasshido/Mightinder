import argparse
import threading

global running_flag

# Setter of global variable
def set_running_state(state):
    global running_flag

    running_flag = state

# Mutex lock to change running flag
def change_running_state():

    global running_flag

    stop_lock.acquire()
    try:
        running_flag = not running_flag
    finally:
        stop_lock.release()

def check_running():
    global running_flag

    stop_lock.acquire()
    try:
        if running_flag:
            value = True
        else:
            value = False
    finally:
        stop_lock.release()

    return value

def check_positive(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError("%s is an invalid positive int value: Allowed values: (1 - 100)" % value)
    return ivalue


# Wrapper to get any function on a thread
def threaded(fn):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapper

# Locks (mutex) for data share between threads
file_lock = threading.Lock()
stop_lock = threading.Lock()
