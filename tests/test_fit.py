# -*- coding: utf-8 -*-
from tests import fixtures
import saccademodel
import unittest2 as unittest  # to support Python 2.6

class TestFit(unittest.TestCase):

    def test_run(self):
        '''
        should be capable to analyze the synthetic saccade
        '''
        X = fixtures.load('synthetic')
        r = saccademodel.fit(X)
        self.assertEqual(len(r['source_points']), 2)
        self.assertEqual(len(r['saccade_points']), 6)
        self.assertEqual(len(r['target_points']), 2)

    # def test_gaps(self):
    #     '''
    #     '''
    #     saccademodel.fit([])

if __name__ == '__main__':
    unittest.main()
