import logging
import coloredlogs
import sys

colors = {
    'cyan':             {'color': 'cyan'},
    'bright_cyan':      {'bright': True, 'color': 'cyan'},
    'bright_blue':      {'bright': True, 'color': 'blue'},
    'green':            {'color': 'green'},
    'yellow':           {'color': 'yellow'},
    'bold_yellow':      {'bold': True, 'color': 'yellow'},
    'magenta':          {'color': 'magenta'},
    'red':              {'color': 'red'},
    'bold_red':         {'bold': True, 'color': 'red'}
}

field_styles = {
    'name':             colors['bright_blue'],
    'funcName':         colors['bright_cyan'],
    'lineno':           colors['yellow'],
    'asctime':          colors['green'],
    'msecs':            colors['green'],
    'process':          colors['green'],
    'levelname':        colors['bold_yellow'],
    'levelno':          colors['bold_yellow'],
}

level_styles = {
    'debug':            colors['bright_cyan'],
    'info':             colors['bright_blue'],
    'warning':          colors['yellow'],
    'error':            colors['red'],
    'critical':         colors['bold_red'],
    'dev':              colors['bold_yellow']
}

DEV = 25

supported_levels = {
    'DEBUG':            logging.DEBUG,
    'INFO':             logging.INFO,
    'WARNING':          logging.WARNING,
    'ERROR':            logging.ERROR,
    'CRITICAL':         logging.CRITICAL,
    'DEV':              DEV,
}

logging_format = (
    '⟨{asctime} {msecs:.0f}ms⟩ [{levelno} {levelname:.3}] › '
    '{name} » {funcName}:{lineno:>3} → {message}'
)

compact_logging_format = (
    '[{levelname:.3}] {name} » {funcName}:{lineno:>3} → {message}'
)

date_format = '%d/%m/%y %I:%M:%S-%p'


def log_dev(self: logging.Logger, msg, *args, **kwargs):
    if self.isEnabledFor(DEV):
        self._log(DEV, msg, args, **kwargs)


def setup_logging(opts):
    """
    USAGE: in any file
        from logging import getLogger
        logger = getLogger(__name__)

        logger.debug("Debug")               # 10
        logger.info("Info")                 # 20
        logger.dev("Dev")                   # 25
        logger.warn("Warn")                 # 30
        logger.warning("Warning")           # 30
        logger.error("Error")               # 40
        logger.exception("Exception")       # 40
        logger.fatal("Fatal")               # 50
        logger.critical("Critical")         # 50
    """

    # Specifically Defined 'DEV' to focus the logging-
    # on development part instead of the whole debug
    logging.addLevelName(DEV, 'DEV')
    logging.Logger.dev = log_dev

    verbose = opts['--verbose'] and logging.INFO
    debug = opts['--debug'] and logging.DEBUG
    level = opts['--log']

    if not (verbose or debug or level):
        logging.root.setLevel(logging.WARNING+100)
        return

    if level and level not in supported_levels:
        raise SystemExit(f"logging level `{level}` is not supported")

    level = level or verbose or debug
    format = (opts['--compact'] and compact_logging_format) or logging_format

    coloredlogs.install(
        level=level,
        fmt=format,
        datefmt=date_format,
        style='{',
        milliseconds=True,
        level_styles=level_styles,
        field_styles=field_styles,
        stream=sys.stderr
    )
