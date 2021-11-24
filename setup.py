#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages


requirements = [
    'bln==0.4.0',
    'requests',
]

test_requirements = [
    'flake8',
    'pytest',
    'pytest-vcr',
    'vcrpy',
]

setup(
    name='bln-etl',
    version='0.1.2',
    description="Utilities for data gathering pipelines for Big Local News.",
    long_description=__doc__,
    author="Serdar Tumgoren",
    author_email='zstumgoren@gmail.com',
    url='https://github.com/biglocalnews/bln-etl',
    packages=find_packages(),
    include_package_data=True,
    #entry_points='''
    #    [console_scripts]
    #    bln-etl=bln_etl.cli:cli
    #''',
    install_requires=requirements,
    license="Apache 2.0 license",
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
