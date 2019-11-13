#!/usr/bin/env python

import os

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()

requires = ['bitshares', 'Crypto', ]

setup(name='onechain-withdraw-atom',
      version='1.0',
      description='The Swiss Army Knife of the Bitcoin protocol.',
      long_description=README,
      classifiers=[
          "Programming Language :: Python",
          "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
      ],
      url='http://121.199.10.86:3030/one.server/onechain-withdraw-atom',
      keywords='bitcoin',
      zip_safe=False,
      install_requires=requires,
      test_suite=""
      )
