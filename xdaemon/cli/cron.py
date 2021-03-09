from os import environ
from crontab import CronTab
from shutil import which
from logging import getLogger

logger = getLogger(__name__)


class Cron:

    @staticmethod
    def get_current_user():
        return environ['USER']

    @staticmethod
    def get_command(job_id):
        xd = which('xd')
        cmd = f'{xd} execute --id {job_id}'
        logger.debug(f'cron commnad: f{cmd}')
        return cmd

    @classmethod
    def setup(cls, job_id, schedule, user=None):

        user = user or cls.get_current_user()

        logger.info("Setting up the Job.")
        logger.debug(f'job-details: {job_id}, {schedule}, {user}')

        with CronTab(user) as tab:
            tab.new(cls.get_command(job_id)) \
               .setall(schedule)

        logger.info("Setup Successfully")

    @classmethod
    def remove(cls, job_id, user=None):

        user = user or cls.get_current_user()

        logger.info("Removing the Job.")
        logger.debug(f'job-details: {job_id}, {user}')

        with CronTab(user) as tab:
            for job in tab.find_command(cls.get_command(job_id)):
                job.delete()

        logger.info("Removed Successfully")
