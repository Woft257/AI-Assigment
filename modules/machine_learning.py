"""
(E) Machine Learning - Học máy
Các thuật toán: Naive Bayes, Decision Tree, Perceptron
"""

from typing import List, Dict, Tuple, Optional
import numpy as np
from collections import Counter, defaultdict


class Perceptron:
    """Perceptron - Đơn vị nhận cảm cơ bản"""

    def __init__(self, learning_rate: float = 0.1):
        self.learning_rate = learning_rate
        self.weights: Optional[np.ndarray] = None
        self.bias: float = 0.0
        self.n_features: int = 0

    def fit(self, X: np.ndarray, y: np.ndarray, epochs: int = 100):
        """
        Train Perceptron
        - X: (n_samples, n_features)
        - y: (n_samples,) - labels 0 or 1
        """
        self.n_features = X.shape[1]
        self.weights = np.zeros(self.n_features)
        self.bias = 0.0

        for _ in range(epochs):
            for xi, yi in zip(X, y):
                # Forward
                prediction = self.predict_one(xi)
                # Update
                update = self.learning_rate * (yi - prediction)
                self.weights += update * xi
                self.bias += update

    def predict_one(self, x: np.ndarray) -> int:
        """Predict cho 1 sample"""
        activation = np.dot(x, self.weights) + self.bias
        return 1 if activation >= 0 else 0

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict cho nhiều samples"""
        return np.array([self.predict_one(x) for x in X])


class DecisionTree:
    """Decision Tree - Cây quyết định"""

    class Node:
        def __init__(self, feature_index=None, threshold=None, left=None, right=None, value=None):
            self.feature_index = feature_index  # Index của feature để split
            self.threshold = threshold          # Ngưỡng split
            self.left = left                    # Nhánh trái
            self.right = right                  # Nhánh phải
            self.value = value                  # Nếu là leaf: nhãn

    def __init__(self, max_depth: int = 10, min_samples_split: int = 2):
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.root: Optional[DecisionTree.Node] = None

    def fit(self, X: np.ndarray, y: np.ndarray):
        """Train Decision Tree"""
        self.root = self._build_tree(X, y, depth=0)

    def _build_tree(self, X: np.ndarray, y: np.ndarray, depth: int) -> Node:
        n_samples, n_features = X.shape
        n_labels = len(np.unique(y))

        # Stopping criteria
        if (depth >= self.max_depth or n_samples < self.min_samples_split or n_labels == 1):
            leaf_value = self._most_common_label(y)
            return Node(value=leaf_value)

        # Find best split
        best_feature, best_threshold = self._find_best_split(X, y)

        if best_feature is None:
            leaf_value = self._most_common_label(y)
            return Node(value=leaf_value)

        # Split
        left_idx = X[:, best_feature] <= best_threshold
        right_idx = X[:, best_feature] > best_threshold

        left = self._build_tree(X[left_idx], y[left_idx], depth + 1)
        right = self._build_tree(X[right_idx], y[right_idx], depth + 1)

        return Node(feature_index=best_feature, threshold=best_threshold, left=left, right=right)

    def _find_best_split(self, X: np.ndarray, y: np.ndarray) -> Tuple[Optional[int], Optional[float]]:
        """Tìm split tốt nhất dựa trên Gini impurity"""
        best_gain = -1
        best_feature, best_threshold = None, None

        n_features = X.shape[1]
        current_gini = self._gini_impurity(y)

        for feature_idx in range(n_features):
            thresholds = np.unique(X[:, feature_idx])
            for threshold in thresholds:
                left_idx = X[:, feature_idx] <= threshold
                right_idx = X[:, feature_idx] > threshold

                if np.sum(left_idx) == 0 or np.sum(right_idx) == 0:
                    continue

                gain = current_gini - (
                    np.sum(left_idx) / len(y) * self._gini_impurity(y[left_idx]) +
                    np.sum(right_idx) / len(y) * self._gini_impurity(y[right_idx])
                )

                if gain > best_gain:
                    best_gain = gain
                    best_feature = feature_idx
                    best_threshold = threshold

        return best_feature, best_threshold

    def _gini_impurity(self, y: np.ndarray) -> float:
        """Tính Gini impurity"""
        if len(y) == 0:
            return 0.0
        counts = Counter(y)
        impurity = 1.0
        for count in counts.values():
            prob = count / len(y)
            impurity -= prob ** 2
        return impurity

    def _most_common_label(self, y: np.ndarray) -> int:
        """Lấy nhãn phổ biến nhất"""
        return Counter(y).most_common(1)[0][0]

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict"""
        return np.array([self._predict_one(x, self.root) for x in X])

    def _predict_one(self, x: np.ndarray, node: Node) -> int:
        if node.value is not None:
            return node.value
        if x[node.feature_index] <= node.threshold:
            return self._predict_one(x, node.left)
        return self._predict_one(x, node.right)


class LinearRegression:
    """Linear Regression (Gradient Descent)"""

    def __init__(self, learning_rate: float = 0.01, epochs: int = 1000):
        self.lr = learning_rate
        self.epochs = epochs
        self.weights: Optional[np.ndarray] = None
        self.bias: float = 0.0

    def fit(self, X: np.ndarray, y: np.ndarray):
        n_samples, n_features = X.shape
        self.weights = np.zeros(n_features)

        for _ in range(self.epochs):
            y_pred = np.dot(X, self.weights) + self.bias
            dw = (1/n_samples) * np.dot(X.T, (y_pred - y))
            db = (1/n_samples) * np.sum(y_pred - y)

            self.weights -= self.lr * dw
            self.bias -= self.lr * db

    def predict(self, X: np.ndarray) -> np.ndarray:
        return np.dot(X, self.weights) + self.bias


def accuracy_score(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Tính accuracy"""
    return np.sum(y_true == y_pred) / len(y_true)


def train_test_split(X: np.ndarray, y: np.ndarray, test_size: float = 0.2, random_state: int = None):
    """Chia train/test"""
    if random_state:
        np.random.seed(random_state)

    n_samples = len(y)
    test_count = int(n_samples * test_size)

    indices = np.random.permutation(n_samples)
    test_idx, train_idx = indices[:test_count], indices[test_count:]

    return X[train_idx], X[test_idx], y[train_idx], y[test_idx]
