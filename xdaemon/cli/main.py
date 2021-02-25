import sys
from docopt import docopt, DocoptExit
from inspect import getdoc

from .parser import YAMLJobParser
from .executor import JobExecutor


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
        print("Executed: show")
        print("Opts:", opts)
        pass

    @staticmethod
    def setup(opts):
        print("Executed: setup")
        print("Opts:", opts)
        pass

    @staticmethod
    def test(opts):
        job = YAMLJobParser.load(opts['-f'])
        executor = JobExecutor(job=job)
        executor.execute()

    @staticmethod
    def remove(opts):
        print("Executed: remove")
        print("Opts:", opts)
        pass

    @staticmethod
    def execute(opts):
        print("Executed: execute")
        print("Opts:", opts)
        pass
