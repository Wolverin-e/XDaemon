import sys
from docopt import docopt, DocoptExit
from inspect import getdoc
import logging

from .parser import YAMLJobParser
from .executor import JobExecutor
from .cron import Cron
from .lookup import JSONDataStore as DataStore
from .local_logging import setup_logging
from .utils import prettify

logger = logging.getLogger(__name__)


def main():
    execute_command(sys.argv[1:])


def get_opts(argv, obj: object):
    doc_str = getdoc(obj)
    try:
        return docopt(
            doc=doc_str,
            argv=argv,
            version="v0.2-ɸ",
            options_first=True
        )
    except DocoptExit as e:
        err = str(e).split('\n')[0]

        usage_header = 'Usage:'
        usage = doc_str.split('\n')
        usage = usage if(usage[0] == usage_header) else usage[2:]
        usage = '\n'.join(usage)

        help_str = f'Err: {err}\n\n{usage}' if(err != usage_header) else usage

        raise SystemExit(help_str)


def execute_command(argv):

    opts = get_opts(argv, Command)
    setup_logging(opts)
    logger.debug(f"opts: \n{prettify(opts)}")
    command = opts["COMMAND"]

    if not command:
        raise SystemExit(getdoc(Command))

    if not hasattr(Command, command):
        raise SystemExit(f"command: {command} is not supported")

    command_function = getattr(Command, command)
    cmd_opts = get_opts(opts['ARGS'], command_function)

    logger.info(f'Executing command: {command}')
    logger.debug(f'command-opts: \n{prettify(cmd_opts)}')

    try:
        command_function(cmd_opts)
    except Exception:
        logger.exception("An uncaught exception occured..")
        exit(1)


class Command:
    """
    Define high-level Jobs and automate them.

    Usage:
      xd [options] [--] [COMMAND] [ARGS...]
      xd -h | --help
      xd --version

    Options:
      -l=<level>, --log=<level>             Log at a given LEVEL when executing.
                                            LEVELS: { DEBUG, INFO, DEV, WARNING,
                                                      ERROR, CRITICAL }
      -v, --verbose                         Enable logging at INFO LEVEL.
      -d, --debug                           Enable logging at DEBUG LEVEL.
      -c, --compact                         Enable Compact logging format,
                                            Used in conjunction with logging enabled.

    Commands:
      show                                  Show the jobs.
      setup [-f <jobfile>]                  Setup a Job.
                                            [Default: ./job.yaml]
      test [-f <jobfile>]                   Test a Job File by executing it.
                                            [Default: ./job.yaml]
      remove (--name <name> | --id <id>)    Remove a job by name or id.
      execute (--name <name> | --id <id>)   Execute a job by name or id.
    """  # NOQA: E501

    @staticmethod
    def show(opts):
        """
        Show already setup jobs.

        Usage:
          show
        """

        DataStore.show_jobs()

    @staticmethod
    def setup(opts):
        """
        Setup a job with a job-file.

        Usage:
          setup [-f <jobfile>]

        Options:
          -f <jobfile>                      Path of the job-file.
                                            [Default: job.yaml]
        """

        job = YAMLJobParser.load(opts['-f'])
        job_id = DataStore.generate_id()
        DataStore.store_job_by_id(job_id, job)
        Cron.setup(job_id, job.schedule)

    @staticmethod
    def test(opts):
        """
        Test a job-file by executing it.

        Usage:
          test [-f <jobfile>]

        Options:
          -f <jobfile>                      Path of the job-file.
                                            [Default: job.yaml]
        """

        job = YAMLJobParser.load(opts['-f'])
        executor = JobExecutor(job)
        executor.execute()

    @staticmethod
    def remove(opts):
        """
        Remove an already setup job.

        Usage:
          remove (--name <name> | --id <id>)

        Options:
          --name <name>                     Name of the Job.
          --id <id>                         ID of the Job.
        """

        job_id = opts['--id'] or DataStore.get_id_from_name(opts['--name'])

        DataStore.remove_job_by_id(job_id)
        Cron.remove(job_id)

    @staticmethod
    def execute(opts):
        """
        Execute an already setup job.

        Usage:
          execute (--name <name> | --id <id>)

        Options:
          --name <name>                     Name of the Job.
          --id <id>                         ID of the Job.
        """

        job_id = opts['--id']
        job_name = opts['--name']
        file = None

        if job_id:
            file = DataStore.search_job_by_id(job_id)['file']
        else:
            file = DataStore.search_job_by_name(job_name)['file']

        job = YAMLJobParser.load(file)
        executor = JobExecutor(job)
        executor.execute()
