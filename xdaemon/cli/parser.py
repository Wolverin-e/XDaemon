import yaml
from pathlib import Path
from logging import getLogger

from .job import Job
from .utils import prettify

logger = getLogger(__name__)


def get_abs_path(file_path):
    return (Path.cwd() / file_path).resolve()


class YAMLJobParser:
    """
    Responsible for parsing a job from job-file.yaml
    """

    @staticmethod
    def get_job_dict(file_path):
        with open(file_path, mode='r') as fh:
            return yaml.safe_load(fh)

    @classmethod
    def load(cls, file_path):
        logger.info(f"Loading the job-file: {file_path}")
        job_dict = cls.get_job_dict(file_path)
        logger.debug(f"Loaded: \n{prettify(job_dict)}")

        return Job(
            file=get_abs_path(file_path),
            name=job_dict['name'],
            schedule=job_dict['schedule'],
            backup=job_dict['backup']
        )
