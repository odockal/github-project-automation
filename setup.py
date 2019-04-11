# -*- coding: utf-8 -*-
'''
Created on Jan 14, 2019

@author: odockal
'''

from distutils.core import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="github-project-automation",
    version="0.0.1",
    author="Ondrej Dockal",
    author_email="odockal@redhat.com",
    description="A little python package providing automation tools for github project release",
    long_description=long_description,
    url="https://github.com/odockal/github-project-automation",
    packages=['github', 'github.utils', 'github.handler', 'github.config'],
    data_files=[('config', ['resources/config.ini'])],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPLv3",
        "Operating System :: OS Independent",
    ],
)
