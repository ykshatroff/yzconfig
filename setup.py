"""A setuptools based setup module for yzconfig

Based on:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path
try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser

PROJECT_DIR = path.dirname(path.abspath(__file__))
PROJECT_INI = path.join(PROJECT_DIR, "project.ini")

config = ConfigParser()
config.read(PROJECT_INI)


def get_config(opt):
    return config.get("project", opt)


def read(*parts):
    filename = path.join(PROJECT_DIR, *parts)
    with open(filename, encoding='utf-8') as fp:
        return fp.read()


REQUIREMENTS_FILE = 'requirements.txt'
REQUIREMENTS = open(path.join(PROJECT_DIR, REQUIREMENTS_FILE)).readlines()

setup(
    name=get_config('name'),
    version=get_config('version'),
    description=get_config('description'),
    long_description=read('README.md'),
    url=get_config('url'),
    author='Yuriy Shatrov',
    author_email='ykshatrov@ya.ru',
    license='Apache Software License',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='config settings',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires=REQUIREMENTS,
    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },
)
