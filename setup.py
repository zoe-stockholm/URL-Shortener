# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


setup(
    name='URL-Shortener',
    version=1,
    description='',
    author='Suyi Jin',
    author_email='jinsuyi@gmail.com',
    include_package_data=True,
    url='https://github.com/zoe-stockholm/URL-Shortener',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 1 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    zip_safe=False,
)
# Usage of setup.py:
# $> python setup.py register # registering package on PYPI
# $> python setup.py build sdist upload # build, make source dist and upload to PYPI