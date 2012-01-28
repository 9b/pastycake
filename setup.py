from distutils.core import setup

setup(
    author='b9',
    author_email='brandon@b9plus.com',
    classifiers= [
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
    name='pastycake',
    packages=['pastycake'],
    requires = [
        'httplib2',
        'Louie',
        'lxml',
    ],
    scripts=['gather.py', 'harvest.py', 'snatch.py'],
    url='http://www.gihub.com/9b/pastycake',
    version='0.1',
)
