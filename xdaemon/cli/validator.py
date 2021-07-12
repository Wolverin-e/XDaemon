import jsonschema
import json
from pathlib import Path
from logging import getLogger

from .job import Job

logger = getLogger(__name__)
FILE_DIR = Path(__file__).parent.resolve()
SCHEMA_FILE = FILE_DIR / "job_schema.json"


def validate_job(job: Job):

    logger.info("Validating the job")

    with open(SCHEMA_FILE) as schema_file:
        job_schema = json.load(schema_file)

    try:
        jsonschema.validate(job.job_dict, job_schema)
    except jsonschema.ValidationError:
        # Show Errors
        logger.info("Validation Failed")
        raise jsonschema.ValidationError

    logger.info("Validation successful")
