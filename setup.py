#!/usr/bin/env python
# -*- coding: utf-8 -*-


# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open


with open('README.md') as readme_file:
    readme = readme_file.read()

setup(
    name='fir_async',
    version='0.1.0',
    description="Plugin for FIR (Fast Incident Response) - async",
    long_description=readme,
    author="Gaetan Crahay",
    author_email='gaetan@crahay.eu',
    url='https://github.com/crahayg/fir_async_plugin',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'django>=1.9',
        'celery'
    ],
    license="GPL v3, see LICENSE",
    zip_safe=False,
    keywords='FIR',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
    ]
)
