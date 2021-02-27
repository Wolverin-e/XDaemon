import json
from json.decoder import JSONDecodeError
from pathlib import Path

from .exceptions import JobAlreadyExists
from .job import Job


FILE_DIR = Path(__file__).parent.resolve()
DATASTORE = FILE_DIR/'job_data.json'


def read_job_data():
    try:
        with open(DATASTORE, "r") as jsondata:
            return json.load(jsondata)
    except (FileNotFoundError, JSONDecodeError):
        return {}


def write_job_data(job_data):
    with open(DATASTORE, "w") as write_json:
        json.dump(job_data, write_json)


def generate_id():
    job_data = read_job_data()
    return int(len(job_data)/2)


def store_job_by_id(job_id, job: Job):
    job_data = read_job_data()
    if job.name in job_data:
        raise JobAlreadyExists(job.name)

    job_data.update({
        job_id: {
            'file': str(job.file),
            'name': job.name
        },
        job.name: job_id
    })
    write_job_data(job_data)


def search_job_by_id(job_id):
    job_data = read_job_data()

    if job_id in job_data:
        return job_data[job_id]
    else:
        return None


def get_id_from_name(job_name):
    job_data = read_job_data()
    if job_name in job_data:
        return str(job_data[job_name])


def search_job_by_name(job_name):
    job_data = read_job_data()

    if job_name in job_data:
        job_id = str(job_data[job_name])
        return job_data[job_id]
    else:
        return None


def remove_job_by_id(job_id):
    job_data = read_job_data()
    if job_id in job_data:
        job_name = job_data[job_id]['name']
        del job_data[job_name]
        del job_data[job_id]
    write_job_data(job_data)


def remove_job_by_name(job_name):
    job_data = read_job_data()
    if job_name in job_data:
        job_id = str(job_data[job_name])
        del job_data[job_name]
        del job_data[job_id]
    write_job_data(job_data)


def show_jobs():
    job_data = read_job_data()
    for key in job_data:
        if type(job_data[key]) == int:
            continue

        print(f'{key} : {job_data[key]["name"]} -> {job_data[key]["file"]}')
