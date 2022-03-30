#!/usr/bin/env python

import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name='bokehView3D',
      version='0.0.2',
      description='View 3D images in Jupyter Notebook',
      author='Zhongnan Fang',
      author_email='zhongnanf@gmail.com',
      url='https://zhongnanf.github.io',
      license="MIT",
      packages=['bokehView3D'],
      long_description=read('README.md'))
