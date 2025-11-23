import time

LOG_LEVEL = 0  # 0 = off, 1 = normal, 2 = verbose

def set_logging(level: int):
    """Set logging level globally."""
    global LOG_LEVEL
    LOG_LEVEL = level


def log(message: str):
    """Normal logging."""
    if LOG_LEVEL >= 1:
        print(f"[LOG] {message}")


def vlog(message: str):
    """Verbose logging."""
    if LOG_LEVEL >= 2:
        print(f"[VERBOSE] {message}")


def time_block(label: str):
    """
    Context manager for timing a block:
        with time_block("selector"):
            ...
    Prints: "[LOG] selector finished in 0.23s"
    """

    class _Timer:
        def __enter__(self):
            self.start = time.time()
            log(f"{label} started…")
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            end = time.time()
            duration = end - self.start
            log(f"{label} finished in {duration:.3f}s")

    return _Timer()
