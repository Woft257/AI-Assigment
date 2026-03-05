"""
Unit tests cho các module AI
"""

import unittest
import numpy as np
import sys
sys.path.append('..')

from modules import search, heuristic_csp, knowledge, bayes, machine_learning


class TestSearch(unittest.TestCase):
    """Test các thuật toán tìm kiếm"""

    def test_bfs_simple(self):
        # TODO: Viết test cho BFS
        pass

    def test_a_star_simple(self):
        # TODO: Viết test cho A*
        pass


class TestHeuristicCSP(unittest.TestCase):
    """Test heuristic và CSP"""

    def test_hill_climbing(self):
        # TODO: Viết test cho Hill Climbing
        pass

    def test_csp_backtracking(self):
        # TODO: Viết test cho CSP
        pass


class TestKnowledge(unittest.TestCase):
    """Test suy luận tri thức"""

    def test_forward_chaining(self):
        # TODO: Viết test cho forward chaining
        pass


class TestBayes(unittest.TestCase):
    """Test Bayes và xác suất"""

    def test_naive_bayes(self):
        # TODO: Viết test cho Naive Bayes
        pass

    def test_bayes_theorem(self):
        prior = 0.01  # 1% mắc bệnh
        likelihood = 0.99  # 99% test đúng khi có bệnh
        evidence = 0.0199  # ~2% dương tính
        posterior = bayes.bayesian_inference(prior, likelihood, evidence)
        self.assertGreater(posterior, 0.5)


class TestML(unittest.TestCase):
    """Test machine learning"""

    def test_perceptron(self):
        # OR problem
        X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
        y = np.array([0, 1, 1, 1])

        clf = machine_learning.Perceptron(learning_rate=0.1)
        clf.fit(X, y, epochs=100)

        predictions = clf.predict(X)
        self.assertTrue(np.array_equal(predictions, y))

    def test_decision_tree(self):
        X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
        y = np.array([0, 1, 1, 0])

        clf = machine_learning.DecisionTree(max_depth=3)
        clf.fit(X, y)

        predictions = clf.predict(X)
        self.assertTrue(np.array_equal(predictions, y))

    def test_accuracy(self):
        y_true = np.array([0, 1, 1, 0])
        y_pred = np.array([0, 1, 0, 0])
        acc = machine_learning.accuracy_score(y_true, y_pred)
        self.assertEqual(acc, 0.75)


if __name__ == '__main__':
    unittest.main()
