import sys
from docopt import docopt, DocoptExit
from inspect import getdoc
import logging
import coloredlogs

from .parser import YAMLJobParser
from .executor import JobExecutor
from .cron import Cron
from .lookup import (
    generate_id,
    get_id_from_name,
    search_job_by_id,
    search_job_by_name,
    show_jobs,
    store_job_by_id,
    remove_job_by_id
)
from .formatting import (
    level_styles,
    field_styles
)


def main():
    execute_command()


def execute_command():
    opts = get_opts(sys.argv[1:])

    commands = [
        'show',
        'setup',
        'test',
        'remove',
        'execute'
    ]

    setup_logging()

    for command in commands:
        if opts[command]:
            getattr(Command, command)(opts)


def get_opts(argv):
    doc_str = getdoc(Command)
    try:
        return docopt(
            doc=doc_str,
            argv=argv,
            version="v0.1"
        )
    except DocoptExit:
        raise SystemExit(doc_str)


def setup_logging():
    """
    USAGE: in any file
        from logging import getLogger
        logger = getLogger(__name__)

        logger.debug("Debug")          # 10
        logger.info("Info")            # 20
        logger.warn("Warn")            # 30
        logger.warning("Warning")      # 30
        logger.error("Error")          # 40
        logger.fatal("Fatal")          # 50
        logger.critical("Critical")    # 50
    """
    logging_format = (
        '⟨{asctime} {msecs:.0f}ms⟩ [{levelno} {levelname:^.3}] › '
        '{name} » {funcName}:{lineno:>3} → {message}'
    )
    date_format = '%d/%m/%y %I:%M:%S-%p'

    coloredlogs.install(
        level=logging.DEBUG,
        fmt=logging_format,
        datefmt=date_format,
        style='{',
        milliseconds=True,
        level_styles=level_styles,
        field_styles=field_styles,
        stream=sys.stderr
    )


class Command:
    """Define high-level Jobs and automate them.

    Usage:
      xd show
      xd setup [-f <jobfile>]
      xd test [-f <jobfile>]
      xd remove (--name <name>| --id <id>)
      xd execute (--name <name>| --id <id>)
      xd -h|--help
      xd --version

    Options:
      -f <jobfile>      Path to a jobfile.yaml
                        [default: job.yaml]
      --name <name>     Name of the Job specified in the jobfile
      --id <id>         Id of the Job given by the system
    """

    @staticmethod
    def show(opts):
        show_jobs()

    @staticmethod
    def setup(opts):
        job = YAMLJobParser.load(opts['-f'])
        job_id = generate_id()
        store_job_by_id(job_id, job)
        Cron.setup(job_id, job.schedule)

    @staticmethod
    def test(opts):
        job = YAMLJobParser.load(opts['-f'])
        executor = JobExecutor(job)
        executor.execute()

    @staticmethod
    def remove(opts):
        job_id = opts['--id'] or get_id_from_name(opts['--name'])

        remove_job_by_id(job_id)
        Cron.remove(job_id)

    @staticmethod
    def execute(opts):
        job_id = opts['--id']
        job_name = opts['--name']
        file = None

        if job_id:
            file = search_job_by_id(job_id)['file']
        else:
            file = search_job_by_name(job_name)['file']

        job = YAMLJobParser.load(file)
        executor = JobExecutor(job)
        executor.execute()
