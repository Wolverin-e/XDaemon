from os import environ
from crontab import CronTab
from shutil import which


class Cron:

    @staticmethod
    def get_current_user():
        return environ['USER']

    @staticmethod
    def get_command(job_id):
        xd = which('xd')
        return f'{xd} execute --id {job_id}'

    @classmethod
    def setup(cls, job_id, schedule, user=None):
        user = user or cls.get_current_user()
        with CronTab(user) as tab:
            tab.new(cls.get_command(job_id)) \
               .setall(schedule)

    @classmethod
    def remove(cls, job_id, user=None):
        user = user or cls.get_current_user()
        with CronTab(user) as tab:
            for job in tab.find_command(cls.get_command(job_id)):
                job.delete()
