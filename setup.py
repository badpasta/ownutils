#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Badpasta <beforgetr@hotmail.com>
# 
# Environment:
# Python by version 2.7.

from setuptools import setup, find_packages


setup(
    name = 'ownutils',
    version = '0.1',
    description = 'DataPool..',
    author = 'Badpasta',
    author_email = 'beforget@hotmail.com',
    url = 'https://github.com/badpasta/ownutils',

    #packages = ['dbpool', 'redispool'],
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    package_data = {'': ['*.py$']},
    install_requires = [
        'momoko',
        'redis',
        'smalltools',
        'psycopg2',
        'tornado'
    ]
    )
