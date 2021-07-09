import os
import zipfile
from pathlib import Path
from datetime import datetime
from logging import getLogger

from .utils import prettify
from .job import Job
from .upload import AzureStorage, IStorage

logger = getLogger(__name__)


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
        self.timestamp = datetime.now().strftime(r"%d-%m-%Y_%H-%M-%S")
        self.storage = None

    def _get_storage_instance(self) -> IStorage:
        if not self.storage:
            self.storage = AzureStorage(self.job.job_dict["creds"])
        return self.storage

    def _backup(self, backup_jobs):

        logger.info("Running the backup command")

        for backup_job in backup_jobs:
            logger.debug(f"\nbackup: {prettify(backup_job)}")

            jobfile_parent = self.job.file.parent.resolve()

            export_file = backup_job['export'].replace(
                r'timestamp',
                self.timestamp
            )
            export_file = (jobfile_parent/export_file).resolve()
            base_dir = (jobfile_parent/backup_job['basedir']).resolve()

            with zipfile.ZipFile(export_file, 'w') as zipf:

                for res in backup_job['resources']:
                    res = base_dir/res

                    if not res.exists():
                        logger.warning(f"zipping: {res} doesn't exist.")
                        continue

                    if res.is_dir():
                        zipdir(res, zipf)
                    else:
                        zipf.write(res, res.name)

            if(('upload' in backup_job) and backup_job['upload']):
                self._get_storage_instance().upload(export_file)

    def _run(self, run_jobs):

        logger.info("Running the run command")

        jobfile_parent = self.job.file.parent.resolve()

        for run_job in run_jobs:
            logger.debug(f"\nrun: {prettify(run_job)}")
            os.system(run_job["exec"])

            if('upload_path' in run_job):
                self._get_storage_instance().upload(
                    (jobfile_parent/run_job['upload_path']).resolve()
                )

    def execute(self):
        logger.info("Executing the job")
        os.chdir(self.job.file.parent.resolve())
        logger.debug(f"Current Directory: {Path(os.curdir).resolve()}")

        for key, value in self.job.job_dict["execute"].items():
            if key == "backup":
                self._backup(value)
            elif key == "run":
                self._run(value)
