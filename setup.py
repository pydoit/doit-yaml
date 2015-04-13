# -*- coding: utf-8 -*-

import sys
from setuptools import setup

setup (
    name = 'doit-yaml',
    version = '0.1.dev0',
    author = 'Eduardo Naufel Schettino',
    author_email = 'schettino72@gmail.com',
    description = 'doit - yaml based task loader',
    url = 'http://github.com/pydoit/doit-yaml',
    keywords = ['doit',],
    platforms = ['any'],
    license = 'MIT',
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries',
    ],

    py_modules=['doit_yaml'],
    install_requires = ['doit', 'pyyaml'],
)
