import os
from concurrent.futures import Future, ThreadPoolExecutor

EXECUTOR_PID, GLOBAL_EXECUTOR = None, None


def run_in_background(func: callable, *args, **kwargs) -> Future:
    """ run func(*args, **kwargs) in background and return Future for its outputs """
    global EXECUTOR_PID, GLOBAL_EXECUTOR
    if os.getpid() != EXECUTOR_PID:
        GLOBAL_EXECUTOR = ThreadPoolExecutor(max_workers=os.environ.get("HIVEMIND_THREADS", float('inf')))
        EXECUTOR_PID = os.getpid()
    return GLOBAL_EXECUTOR.submit(func, *args, **kwargs)


def increase_file_limit(new_soft=2 ** 15, new_hard=2 ** 15):
    """ Increase the maximum number of open files. On Linux, this allows spawning more processes/threads. """
    try:
        import resource  # note: local import to avoid ImportError for those who don't have it
        soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
        print(f"Increasing file limit - soft {soft}=>{new_soft}, hard {hard}=>{new_hard}")
        return resource.setrlimit(resource.RLIMIT_NOFILE, (max(soft, new_soft), max(hard, new_hard)))
    except Exception as e:
        warn(f"Failed to increase file limit: {e}")