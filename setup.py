#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from setuptools import find_packages, setup
import googleAuth

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='googleAuth',
    version=googleAuth.__version__,
    #packages=find_packages(),
    packages=['googleAuth', 'googleAuth.migrations'], 
    include_package_data=True,
    install_requires=[
        'google-api-python-client'
    ], 
    license=googleAuth.__license__,  # example license
    description='Some django google auth utils',
    long_description=README,
    url=googleAuth.__url__,
    author=googleAuth.__author__,
    author_email=googleAuth.__author_email__,
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.10',  # keep updated "X.Y" as appropriate
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ' + googleAuth.__license__,  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        # Replace these appropriately if you are stuck on Python 2.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
