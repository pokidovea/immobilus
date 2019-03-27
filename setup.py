#!/usr/bin/env python

from setuptools import setup

with open('README.rst', 'r') as f:
    long_description = f.read()

setup(
    name='immobilus',
    version='1.4.3',
    description='Say `Immobilus!` to freeze your tests',
    long_description=long_description,
    author='Eugene Pokidov',
    author_email='pokidovea@gmail.com',
    url='https://github.com/pokidovea/immobilus',
    packages=['immobilus'],
    install_requires=['python-dateutil'],
    include_package_data=True,
    license='Apache 2.0',
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
