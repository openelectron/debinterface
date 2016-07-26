#!/usr/bin/env python

from setuptools import setup, find_packages


REQUIREMENTS = [
]

DEP = [
]

TEST_REQUIREMENTS = [
]

pyxed = []
pack = find_packages(exclude=["test"])

setup(
    name="debinterface",
    version="2.2.0",
    description=" A simple Python library for dealing with the /etc/network/interfaces file in most Debian based distributions.",
    ext_modules=pyxed,
    packages=pack,
    install_requires=REQUIREMENTS,
    dependency_links=DEP,
    # tests
    test_suite="test",
    tests_require=TEST_REQUIREMENTS,
)

