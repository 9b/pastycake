from sys import version_info

from setuptools import setup


_ALWAYS_REQUIRED_PACKS = [
    'distribute',
    'httplib2',
    'Louie',
    'lxml',
]


def _required_packages():
    res = _ALWAYS_REQUIRED_PACKS
    vers = version_info[:2]

    # argparse is part of the stdlib in Python2.x >= 2.7 and Python3.x >= 3.2
    if vers < (2, 7) or (3, 0) <= vers < (3, 2):
        res.append('argparse')

    return res


setup(
    author='b9',
    author_email='brandon@b9plus.com',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: Communications",
        "Topic :: Internet",
        "Topic :: Security",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Filters"
    ],
    description='scan pastes for interesting stuff',
    entry_points={
        'console_scripts': [
            'pastycake-snatch = pastycake.gather:snatch',
            'pastycake-harvest = pastycake.gather:harvest',
            'pastycake = pastycake.gather:main',
        ],
        'pastycake': [
            'sources:Pastebin = pastycake.pastebin_source:PastebinSource',
            'sources:Pastie = pastycake.pastie_source:PastieSource',
            'storage:Sqlite = pastycake.sqlite_backend:SqliteBackend',
            'storage:Text = pastycake.text_backend:TextBackend',
            'notify:Cli = pastycake.cli_notifier:CliNotifier',
            'notify:Mail = pastycake.mailer:Mailer',
        ],
        'pastycake.ext': [
            'storage:MongoDB = pastycake.mongodb_backend:MongoBackend [MongoDB]',
        ]
    },
    extras_require={
        'MongoDB': ['pymongo'],
    },
    name='pastycake',
    packages=['pastycake'],
    install_requires=_required_packages(),
    url='http://www.gihub.com/9b/pastycake',
    use_2to3=True,
    version='0.1',
)
