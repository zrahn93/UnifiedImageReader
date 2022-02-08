import os
from setuptools import setup

def parse_requirements(filename):
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]

install_reqs = parse_requirements("./requirements.txt")

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="unified_image_reader",
    version="0.0.1",
    author="Adin Solomon",
    author_email="adinbsolomon@gmail.com",
    description=(
        "todo lol"),
    license="MIT",
    keywords="todo",
    packages=[''],
    long_description=read('README.md'),
    install_requires=install_reqs,
)