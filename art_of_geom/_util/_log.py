__all__ = 'STDOUT_HANDLER',


from logging import Formatter, StreamHandler
import sys


# handler for logging to StdOut
STDOUT_HANDLER = StreamHandler(sys.stdout)

STDOUT_HANDLER.setFormatter(
    Formatter(
        fmt='%(asctime)s   %(levelname)s   %(name)s:   %(message)s\n',
        datefmt='%Y-%m-%d %H:%M'))
