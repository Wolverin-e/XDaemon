from os import environ
from crontab import CronTab
from shutil import which


CURRENT_USER = environ['USER']


class Cron:

	@staticmethod
	def get_command(jobid):
		xd = which('xd')
		return f'{xd} execute --id {jobid}'

	@classmethod
	def setup(cls, jobid, schedule, user=CURRENT_USER):
		with CronTab(user) as tab:
			tab.new(cls.get_command(jobid)) \
				.setall(schedule)

	@classmethod
	def remove(cls, jobid, user=CURRENT_USER):
		with CronTab(user) as tab:
			for job in tab.find_command(cls.get_command(jobid)):
				job.delete()
