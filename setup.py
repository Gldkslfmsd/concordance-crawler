# -*- coding: utf-8 -*-

from setuptools import setup

setup(name='ConcordanceCrawler',
      version='0.0.0.0.1',
      description='A module for automatic concordance extraction from the Internet',
      long_description='TODO',
      author='Dominik Macháček',
      author_email='gldkslfmsd@gmail.com',
      url='https://github.com/Gldkslfmsd',
      py_modules=['usage'],
      packages=['ConcordanceCrawler'],
      entry_points={'console_scripts': ['ConcordanceCrawler	= ConcordanceCrawler.app:main']},
#      package_data={
#          'ConcordanceCrawler': ['config.cfg'],
#      },
      install_requires=['GoogleScraper','beautifulsoup4','dict2xml']
)
