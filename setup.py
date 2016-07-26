#!/usr/bin/env python

from setuptools import setup, find_packages


REQUIREMENTS = [
]

pack = find_packages(exclude=["test"])

setup(
    name="debinterface",
    version="2.2.0",
    description=" A simple Python library for dealing with the /etc/network/interfaces file in most Debian based distributions.",
    packages=pack,
    install_requires=REQUIREMENTS,
    test_suite="test",
)

