import os
import zipfile
from pathlib import Path
from datetime import datetime

from .job import Job


def zipdir(path: Path, zipf: zipfile.ZipFile):

    parent_dir = str(path.parent)+'/'

    for root, dirs, files in os.walk(path):

        relative_root = Path(root.replace(parent_dir, ''))
        zipf.write(root, relative_root)

        for file in files:
            zipf.write(Path(root)/file, relative_root/file)


class JobExecutor:
    """
    Responsible for executing a job
    """

    def __init__(self, job: Job):
        self.job = job

    def execute(self):
        # For now the by default job is backup
        # Just zipping

        for backup_job in self.job.backup:

            jobfile_parent = self.job.file.parent.resolve()

            timestamp = datetime.now().strftime(r"%d-%m-%Y_%H-%M-%S")
            export_file = backup_job['export'].replace(r'timestamp', timestamp)
            export_file = (jobfile_parent/export_file).resolve()
            base_dir = (jobfile_parent/backup_job['basedir']).resolve()

            with zipfile.ZipFile(export_file, 'w') as zipf:

                for res in backup_job['resources']:
                    res = base_dir/res

                    if not res.exists():
                        continue

                    if res.is_dir():
                        zipdir(res, zipf)
                    else:
                        zipf.write(res, res.name)
