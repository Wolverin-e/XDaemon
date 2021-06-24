import json
from json.decoder import JSONDecodeError
import os
from pathlib import Path
from logging import getLogger
from enum import Enum

from .exceptions import JobAlreadyExists, PermissionError
from .job import Job
from .utils import prettify

logger = getLogger(__name__)
FILE_DIR = Path(__file__).parent.resolve()
DATASTORE = FILE_DIR/'job_data.json'


class Keys(str, Enum):
    jobs = "jobs"
    names = "names"
    enabled = "enabled"
    file = "file"
    name = "name"
    user = "user"


class JSONDataStore():
    """
        Responsible for interaction with a JSON-File datastore.
    """

    @staticmethod
    def read_job_data():

        logger.info("Reading the datastore.")

        try:
            with open(DATASTORE, "r") as jsondata:
                ds = json.load(jsondata)
                logger.debug(f"Read: \n{prettify(ds)}")
                return ds
        except (FileNotFoundError, JSONDecodeError):
            logger.warning(f"{DATASTORE} missing")
            return {
                Keys.jobs: {},
                Keys.names: {},
                Keys.enabled: []
            }

    @staticmethod
    def write_job_data(job_data):

        logger.info("Writing to the Datastore.")
        logger.debug(f"job_data: \n{prettify(job_data)}")

        with open(DATASTORE, "w") as write_json:
            json.dump(job_data, write_json)

    @classmethod
    def generate_id(cls):

        job_data = cls.read_job_data()
        id = len(job_data[Keys.jobs])

        logger.debug(f"Generated id: {id}")

        return id

    @classmethod
    def store_job_by_id(cls, job_id, job: Job):

        logger.info("Storing the job.")
        logger.debug(f"id: {job_id} \n job: {job.name}")

        job_data = cls.read_job_data()
        if job.name in job_data[Keys.names]:
            raise JobAlreadyExists(job.name)

        jobs_updates = {
            job_id: {
                Keys.file: str(job.file),
                Keys.name: job.name,
                Keys.user: os.environ['USER']
            }
        }

        names_update = {
            job.name: job_id
        }

        logger.debug(f"updates: \njobs:{prettify(jobs_updates)} \n\
                       names:{prettify(names_update)}")

        job_data[Keys.names].update(names_update)
        job_data[Keys.jobs].update(jobs_updates)
        job_data[Keys.enabled].append(job_id)

        cls.write_job_data(job_data)

    @classmethod
    def search_job_by_id(cls, job_id):

        job_id = str(job_id)  # Necessary for JSON Keys

        logger.info("Searching the job by id.")
        logger.debug(f"id: {job_id}")

        job_data = cls.read_job_data()

        if job_id in job_data[Keys.jobs]:
            return job_data[Keys.jobs][job_id]
        else:
            return None

    @classmethod
    def get_id_from_name(cls, job_name):
        job_data = cls.read_job_data()
        if job_name in job_data[Keys.names]:
            return str(job_data[job_name])

    @classmethod
    def search_job_by_name(cls, job_name):

        logger.info("Searching the job by name")
        logger.debug(f"name: {job_name}")

        job_data = cls.read_job_data()

        if job_name in job_data[Keys.names]:
            job_id = str(job_data[Keys.names][job_name])
            return job_data[Keys.jobs][job_id]
        else:
            return None

    @classmethod
    def remove_job_by_id(cls, job_id):

        job_id = str(job_id)  # Necessary for JSON Keys

        logger.info("Removing the job..")
        logger.debug(f"id: {job_id}")

        job_data = cls.read_job_data()
        if job_id in job_data[Keys.jobs]:

            job_user = job_data[Keys.jobs][job_id][Keys.user]
            if os.environ['USER'] != job_user:
                raise PermissionError(f"The Job was setup by: {job_user}")

            job_name = job_data[Keys.jobs][job_id][Keys.name]
            del job_data[Keys.names][job_name]
            del job_data[Keys.jobs][job_id]

            # Type-Conversion Necessary for searching in a list of int
            job_id = int(job_id)
            if(job_id in job_data[Keys.enabled]):
                job_data[Keys.enabled].remove(job_id)

        cls.write_job_data(job_data)

    @classmethod
    def show_jobs(cls):

        jobs = cls.read_job_data()
        jobs = jobs[Keys.jobs]

        for job_id in jobs:

            job = jobs[job_id]

            print('{} : {} : {} -> {}'.format(
                job_id,
                job[Keys.user],
                job[Keys.name],
                job[Keys.file]
            ))
