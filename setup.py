#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

'''
  Packaging
  ---------

  :copyright (c) 2014 Xavier Bruhiere
  :license: Apache 2.0, see LICENSE for more details.
'''

import setuptools
from pyconsul import __version__, __author__, __licence__


REQUIREMENTS = [
    'requests>=2.3.0'
]


def long_description():
    ''' Safely provide to setup.py the project README.md '''
    try:
        with open('README.md') as readme_file:
            return readme_file.read()
    except IOError:
        return "failed to read README.md"


setuptools.setup(
    name='pyconsul',
    version=__version__,
    description='Python client for Consul (http://www.consul.io)',
    author=__author__,
    author_email='xavier.bruhiere@gmail.com',
    packages=setuptools.find_packages(),
    long_description=long_description(),
    license=__licence__,
    install_requires=REQUIREMENTS,
    url="https://github.com/hackliff/pyconsul",
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Operating System :: OS Independent',
        'Topic :: Documentation',
    ]
)
