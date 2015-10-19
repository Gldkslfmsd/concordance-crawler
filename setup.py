# -*- coding: utf-8 -*-

# TODO!!!!
# this doesn't work!!!

from setuptools import setup
import re

# taken from GoogleScraper:
version = re.search(
	   "^__version__\s*=\s*'(.*)'",
		 open('ConcordanceCrawler/__init__.py').read(),
				    re.M).group(1)

setup(name='ConcordanceCrawler',
      version=version,
      description='A module for automatic concordance extraction from the Internet',
      long_description='TODO',
      author='Dominik Macháček',
      author_email='gldkslfmsd@gmail.com',
      url='https://github.com/Gldkslfmsd',
      py_modules=['usage'],
      packages=['ConcordanceCrawler'],
      entry_points={'console_scripts': ['ConcordanceCrawler = ConcordanceCrawler.app.app:main']},
      install_requires=['GoogleScraper','beautifulsoup4','dict2xml']
)
