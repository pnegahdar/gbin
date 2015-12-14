#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of gbin.
# https://github.com/pnegahdar/gbin

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Parham Negahdar <pnegahdar@gmail.com>

from setuptools import setup, find_packages


tests_require = [
    'mock',
    'nose',
    'coverage',
    'yanc',
    'preggy',
    'tox',
    'ipdb',
    'coveralls',
    'sphinx',
]

setup(
    name='gbin',
    version='0.2.6',
    description='a git based command discoverer and executor',
    long_description='''
a git based command discoverer and executer
''',
    keywords='management commands git inenv gbin discovery cli python',
    author='Parham Negahdar',
    author_email='pnegahdar@gmail.com',
    url='https://github.com/pnegahdar/gbin',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2.7',
        'Operating System :: OS Independent',
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        # add your dependencies here
        # remember to use 'package-name>=x.y.z,<x.y+1.0' notation (this way you get bugfixes)
        'inenv>=0.6.2',
        'click>=4.0',
        'virtualenv>=13.0.3'],
    extras_require={
        'tests': tests_require,
    },
    entry_points={
        'console_scripts': [
            # add cli scripts here in this form:
            'gbin=gbin.cli:run_cli',
        ],
    },
)
