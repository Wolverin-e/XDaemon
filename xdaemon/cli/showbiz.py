from enum import Enum
from tabulate import tabulate

from .lookup import JSONDataStore, Keys as DataStoreKeys


class Keys(str, Enum):
    all = "all"
    active = "active"
    inactive = "inactive"


class ShowBiz:

    jobs_headers = [
        "ID",
        "FILE",
        "NAME",
        "USER",
        "STATUS"
    ]

    jobs_headers_filtered = [
        "ID",
        "FILE",
        "NAME",
        "USER"
    ]

    @staticmethod
    def _get_structured_jobs(jobs_type=Keys.all):
        jobs_data = JSONDataStore.read_job_data()

        jobs = []
        enabled_jobs = jobs_data[DataStoreKeys.enabled]

        if jobs_type == Keys.all:
            for job_id, job in jobs_data[DataStoreKeys.jobs].items():
                jobs.append([
                    job_id,
                    job[DataStoreKeys.file],
                    job[DataStoreKeys.name],
                    job[DataStoreKeys.user],
                    "ENABLED" if int(job_id) in enabled_jobs else "DISABLED"
                ])
        else:

            jobs_to_show = []

            all_jobs = map(
                lambda x: int(x),
                jobs_data[DataStoreKeys.jobs].keys()
            )

            if jobs_type == Keys.active:
                jobs_to_show = enabled_jobs
            else:
                jobs_to_show = set(all_jobs).difference(set(enabled_jobs))

            for job_id in jobs_to_show:
                job = jobs_data[DataStoreKeys.jobs][str(job_id)]
                jobs.append([
                    job_id,
                    job[DataStoreKeys.file],
                    job[DataStoreKeys.name],
                    job[DataStoreKeys.user],
                ])

        return jobs

    @classmethod
    def show_jobs(cls, jobs_type=Keys.all):

        jobs = cls._get_structured_jobs(jobs_type=jobs_type)

        if jobs_type == Keys.all:
            print(
                tabulate(
                    jobs,
                    headers=cls.jobs_headers,
                    tablefmt="fancy_grid"
                )
            )
        else:
            print(
                tabulate(
                    jobs,
                    headers=cls.jobs_headers_filtered,
                    tablefmt="fancy_grid"
                )
            )
