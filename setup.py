#!/usr/bin/env python
#
# Copyright 2014 Xavier Bruhiere


import setuptools
from pyconsul import __version__, __author__, __licence__


requires = [
    'requests>=2.2.1'
]


def long_description():
    try:
        #with codecs.open(readme, encoding='utf8') as f:
        with open('README.md') as f:
            return f.read()
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
    install_requires=requires,
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
