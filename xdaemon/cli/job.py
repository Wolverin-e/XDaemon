from pathlib import Path


class Job:
    """
    Responsible for containing Job-Data
    """

    def __init__(self, file: Path, name, schedule, backup):
        self.file = file
        self.name = name
        self.schedule = schedule
        self.backup = backup
