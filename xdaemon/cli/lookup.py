import json
from json.decoder import JSONDecodeError
import os
from pathlib import Path
from logging import getLogger

from .exceptions import JobAlreadyExists, PermissionError
from .job import Job
from .utils import prettify

logger = getLogger(__name__)
FILE_DIR = Path(__file__).parent.resolve()
DATASTORE = FILE_DIR/'job_data.json'


class JSONDataStore():
    """
        Responsible for interaction with a JSON-File datastore.
    """

    def read_job_data():

        logger.info("Reading the datastore.")

        try:
            with open(DATASTORE, "r") as jsondata:
                ds = json.load(jsondata)
                logger.debug(f"Read: \n{prettify(ds)}")
                return ds
        except (FileNotFoundError, JSONDecodeError):
            logger.warning(f"{DATASTORE} missing")
            return {}

    def write_job_data(job_data):

        logger.info("Writing to the Datastore.")
        logger.debug(f"job_data: \n{prettify(job_data)}")

        with open(DATASTORE, "w") as write_json:
            json.dump(job_data, write_json)

    @classmethod
    def generate_id(cls):

        job_data = cls.read_job_data()
        id = int(len(job_data)/2)

        logger.debug(f"Generated id: {id}")

        return id

    @classmethod
    def store_job_by_id(cls, job_id, job: Job):

        logger.info("Storing the job.")
        logger.debug(f"id: {id} \n job: {job_id}")

        job_data = cls.read_job_data()
        if job.name in job_data:
            raise JobAlreadyExists(job.name)

        updates = {
            job_id: {
                'file': str(job.file),
                'name': job.name,
                'user': os.environ['USER']
            },
            job.name: job_id
        }

        logger.debug(f"updates: {prettify(updates)}")

        job_data.update(updates)
        cls.write_job_data(job_data)

    @classmethod
    def search_job_by_id(cls, job_id):

        logger.info("Searching the job by id.")
        logger.debug(f"id: {job_id}")

        job_data = cls.read_job_data()

        if job_id in job_data:
            return job_data[job_id]
        else:
            return None

    @classmethod
    def get_id_from_name(cls, job_name):
        job_data = cls.read_job_data()
        if job_name in job_data:
            return str(job_data[job_name])

    @classmethod
    def search_job_by_name(cls, job_name):

        logger.info("Searching the job by name")
        logger.debug(f"name: {job_name}")

        job_data = cls.read_job_data()

        if job_name in job_data:
            job_id = str(job_data[job_name])
            return job_data[job_id]
        else:
            return None

    @classmethod
    def remove_job_by_id(cls, job_id):

        logger.info("Removing the job..")
        logger.debug(f"id: {job_id}")

        job_data = cls.read_job_data()
        if job_id in job_data:

            job_user = job_data[job_id]['user']
            if os.environ['USER'] != job_user:
                raise PermissionError(f"The Job was setup by: {job_user}")

            job_name = job_data[job_id]['name']
            del job_data[job_name]
            del job_data[job_id]
        cls.write_job_data(job_data)

    @classmethod
    def show_jobs(cls):
        job_data = cls.read_job_data()
        for key in job_data:
            if type(job_data[key]) == int:
                continue

            job = job_data[key]
            print(f'{key} : {job["user"]} : {job["name"]} -> {job["file"]}')
