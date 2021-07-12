from pathlib import Path


class Job:
    """
    Responsible for containing Job-Data
    """

    def __init__(self, file: Path, name, schedule, job_dict):
        self.file = file
        self.name = name
        self.schedule = schedule
        self.job_dict = job_dict
