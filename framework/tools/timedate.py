import time


def get_sec_time():
    return int(time.time())

def get_ms_time():
    return int(round(time.time() * 1000))