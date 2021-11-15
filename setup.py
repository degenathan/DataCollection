"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup

APP = ['/Users/jackiedegen/Google '
 'Drive/research/datacollection/datacollection-api.py']
DATA_FILES = ['city_api_list.csv']
OPTIONS = {}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)