# -*- coding: utf-8 -*-

from setuptools import setup
import re

# taken from GoogleScraper:
version = re.search(
	   "^__version__\s*=\s*'(.*)'",
		 open('ConcordanceCrawler/__init__.py').read(),
				    re.M).group(1)

#f = open("README.md","r")
description = ""#"f.read()
#f.close()

setup(name='ConcordanceCrawler',
      version=version,
      description='A module for automatic concordance extraction from the Internet',
      long_description=description,
      author='Dominik Macháček',
      author_email='gldkslfmsd@gmail.com',
      url='https://github.com/Gldkslfmsd/concordance-crawler',
			download_url = 'http://pypi.python.org/pypi/ConcordanceCrawler',
      py_modules=['usage'],
			keywords='concordance, crawling, corpus, Internet',
			license='MIT',
			platforms='any',
      packages=['ConcordanceCrawler','ConcordanceCrawler.app','ConcordanceCrawler.core',
				'ConcordanceCrawler.core.eng_detect',
				'ConcordanceCrawler.tests',],
      entry_points={'console_scripts': [
				'ConcordanceCrawler = ConcordanceCrawler.app.app:main',
				]
				},
      install_requires=['cssselect','lxml','requests','beautifulsoup4','simplejson','six','segtok','regex','stopit'],
			test_suite='ConcordanceCrawler.tests',
			classifiers = [
				"Development Status :: 5 - Production/Stable",
				"Environment :: Console",
				"Intended Audience :: Science/Research",
				"Operating System :: OS Independent",
				"Programming Language :: Python :: 2.7",
				"Programming Language :: Python :: 3.2",
				"Programming Language :: Python :: 3.3",
				"Programming Language :: Python :: 3.4",
				"Programming Language :: Python :: 3.5",
				"Topic :: Text Processing :: Linguistic",
				"Natural Language :: English",
			],
)
