__all__ = 'STDOUT_HANDLER', 'logger'


from logging import \
    getLogger, Logger, \
    Handler, StreamHandler, Formatter, \
    DEBUG, INFO
import sys
from typing import Optional

import art_of_geom._util._debug


# handler for logging to StdOut
STDOUT_HANDLER = StreamHandler(sys.stdout)

STDOUT_HANDLER.setFormatter(
    Formatter(
        fmt='%(asctime)s   %(levelname)s   %(name)s:   %(message)s\n',
        datefmt='%Y-%m-%d %H:%M'))


def logger(name: str, /, *handlers: Handler, level: Optional[int] = INFO) -> Logger:
    l = getLogger(name=name)

    for handler in handlers:
        l.addHandler(handler)

    if art_of_geom._util._debug.ON:
        level = DEBUG
    elif level is None:
        level = INFO
    l.setLevel(level)

    return l
