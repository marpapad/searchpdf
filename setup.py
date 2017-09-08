# -*- coding: utf-8 -*-
"""
Created on Tue Aug 22 22:58:30 2017

@author: DELL PM
"""

from setuptools import setup,find_packages


setup(

     name='searchpdf',

     version='0.3.3', 

     description = 'converts non-searchable pdf files to searchable ones',

     author = 'marpapad',

     author_email='marypapadaki13@gmail.com',

     url='https://github.com/marpapad/searchpdf.git',
     
     download_url = 'https://github.com/marpapad/searchpdf/archive/0.1.tar.gz',

     packages=find_packages(),
         
     install_requires=['Click'],
     classifiers=['Programming Language :: Python :: 3'],
     
     entry_points='''
        [console_scripts]
        searchpdf=searchpdf:main
    '''
    ) 
