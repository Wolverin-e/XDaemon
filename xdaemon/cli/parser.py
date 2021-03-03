import yaml
from pathlib import Path

from .job import Job


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
        job_dict = cls.get_job_dict(file_path)
        return Job(
            file=get_abs_path(file_path),
            name=job_dict['name'],
            schedule=job_dict['schedule'],
            backup=job_dict['backup']
        )
