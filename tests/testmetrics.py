import unittest

from etllib.metrics import Metrics

class TestMetrics(unittest.TestCase):

    def setUp(self):
        pass

    def test_intersect(self): 
        self.assertEqual(
            Metrics.intersection(
                [1, 3, 4], 
                [1, 2, 5]
            ), 1
        )
        self.assertEqual(
            Metrics.intersection(
                [0, 3, 4], 
                [1, 2, 5]
            ), -1
        )
        self.assertEqual(
            Metrics.intersection(
                [], 
                []
            ), -1
        )

    def test_jaccard(self): 
        self.assertEqual(
            Metrics.jaccard(
                [1, 3, 5], 
                [1, 2, 5]
            ), 0.5
        )
        self.assertEqual(
            Metrics.jaccard(
                [], 
                []
            ), -1
        )

    def test_lte(self): 
        self.assertEqual(Metrics.lte(5, 4), -1)
        self.assertEqual(Metrics.lte(4, 5),  1)

    def test_gte(self): 
        self.assertEqual(Metrics.gte(5, 4),  1)
        self.assertEqual(Metrics.gte(4, 5), -1)



if __name__ == '__main__':

    unittest.main()