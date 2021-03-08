from setuptools import setup, find_packages
import pathlib


def get_readme() -> str:
    current_dir = pathlib.Path(__file__).parent.resolve()
    readme_path = current_dir/"README.md"
    return readme_path.read_text('utf-8')


setup(
    name='XDaemon',
    version='0.0.1',
    description='Executable of Backup Daemon',
    long_description=get_readme(),
    long_description_content_type='text/markdown',
    author='Mitul Patel',
    author_email='patel.6@iitj.ac.in',
    keywords='backup, autoexecution, automation',
    packages=find_packages(
        include=('xdaemon*', )
    ),
    # >= 3.3 due to shutil.which in cron.py
    python_requires='>=3.3, <4',
    entry_points={
        'console_scripts': [
            'xd=xdaemon.cli.main:main',
        ],
    },
    install_requires=[
        "docopt==0.6.2",
        "PyYAML==5.4.1",
        "python-crontab==2.5.1",
        "coloredlogs==15.0"
    ],
    extras_require={
        'dev': [
            'flake8',
            'autopep8'
        ],
    },
    # classifiers=[
    # 	'Development Status :: 1 - Planning',
    # 	'Intended Audience :: Developers',
    # 	'Intended Audience :: System Administrators',
    # 	'Programming Language :: Python :: 3'
    # ],
    # url='',
    # project_urls={
    # 	'Bug Reports': '',
    # 	'Say Thanks!': '',
    # 	'Source': '',
    # },
)
