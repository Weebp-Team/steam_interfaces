from io import open
from setuptools import setup

"""
:authors: Tarodictrl
:license: MIT License, see LICENSE file
:copyright: (c) 2023 Tarodictrl
"""

version = '0.2.8'

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='steam_interfaces',
    version=version,

    author='Tarodictrl',
    author_email='vudi600@gmail.com',

    description=(
        u'Python library for working with the Steam API.'
    ),
    long_description=long_description,
    long_description_content_type='text/markdown',

    url='https://github.com/Weebp-Team/steamapi',
    download_url='https://github.com/Weebp-Team/steamapi/archive/main.zip',

    license='MIT License, see LICENSE file',

    packages=['steam_interfaces'],
    install_requires=['requests'],

    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: CPython',
    ]
)