# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='BusLane',
    version='0.1.0',
    description='Dublin Bus Web Application',
    long_description=readme,
    author='Alan Treanor',
    author_email='alan.treanor@ucdconnect.ie',
    url='https://github.com/atreanor/BusLane',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

