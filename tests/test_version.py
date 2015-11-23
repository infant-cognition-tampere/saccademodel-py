# -*- coding: utf-8 -*-
import saccademodel
import unittest2 as unittest  # to support Python 2.6
import pkg_resources  # part of setuptools

class TestVersion(unittest.TestCase):

    def test_equal(self):
        '''
        should have version that match package
        '''
        setuppy_version = pkg_resources.require('saccademodel')[0].version
        self.assertEqual(saccademodel.version, setuppy_version)

if __name__ == '__main__':
    unittest.main()
