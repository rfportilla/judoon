try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import os
import sys
import unittest

def discoverTests():
    filePatterns = ['*_unit_tests.py', '*_functional_tests.py']
    setupFile = sys.modules['__main__'].__file__
    setupDir = os.path.abspath(os.path.dirname(setupFile))
    testsDir = os.path.join(setupDir, 'tests')
    testSuite = unittest.TestSuite(tests=())
    for pattern in filePatterns:
        tests = unittest.defaultTestLoader.discover(testsDir, pattern)
        testSuite.addTests(tests)
    return testSuite

setup(
    name='judoon',
    version='1',
    description='Audit script for Cisco switches',
    author='Fabian Portilla',
    author_email='rfportilla@yahoo.com',
    url='',
    packages=['judoon'],
    scripts=[],
    data_files=[],
    install_requires=['SHUtils', 'xmltodict', 'dicttoxml'],
    tests_require=['mock'],
    test_suite='__main__.discoverTests',
)
