"""
(D) Bayesian Networks & Probability - Mạng Bayes và Xác suất
Các thuật toán: Bayes Network, Naive Bayes, Bayesian Inference
"""

from typing import Dict, List, Optional, Any
import numpy as np
from collections import defaultdict


class Variable:
    """Biến ngẫu nhiên"""

    def __init__(self, name: str, values: List):
        self.name = name
        self.values = values  # Các giá trị có thể

    def __repr__(self):
        return self.name


class ConditionalProbability:
    """Phân phối xác suất có điều kiện P(X | Parents)"""

    def __init__(self, variable: Variable, parents: List[Variable] = None):
        self.variable = variable
        self.parents = parents or []
        self.probabilities: Dict = {}

    def set_probability(self, condition: tuple, value: str, prob: float):
        """Thiết lập P(X=value | Parents=condition)"""
        self.probabilities[(condition, value)] = prob

    def get_probability(self, condition: tuple, value: str) -> float:
        """Lấy P(X=value | Parents=condition)"""
        return self.probabilities.get((condition, value), 0.0)


class BayesianNetwork:
    """Mạng Bayes"""

    def __init__(self):
        self.variables: Dict[str, Variable] = {}
        self.cpds: Dict[str, ConditionalProbability] = {}  # Conditional Probability Distributions
        self.structure: Dict[str, List[str]] = defaultdict(list)  # parent -> children

    def add_variable(self, variable: Variable):
        """Thêm biến"""
        self.variables[variable.name] = variable

    def add_edge(self, parent: str, child: str):
        """Thêm cạnh có hướng parent -> child"""
        self.structure[parent].append(child)

    def add_cpd(self, cpd: ConditionalProbability):
        """Thêm CPD"""
        self.cpds[cpd.variable.name] = cpd

    def query(self, query_var: str, evidence: Dict[str, str] = None) -> Dict[str, float]:
        """
        Inference - Suy luận với bằng chứng
        TODO: Implement exact inference (枚举/变量消除) or approximate (粒子采样)
        """
        # TODO: Implement inference
        pass


class NaiveBayesClassifier:
    """Naive Bayes Classifier"""

    def __init__(self):
        self.class_probs: Dict = {}  # P(Class)
        self.feature_probs: Dict = {}  # P(Feature|Class)
        self.classes: List = []

    def fit(self, X: np.ndarray, y: np.ndarray):
        """
        Train Naive Bayes
        - X: numpy array (n_samples, n_features)
        - y: numpy array (n_samples,)
        """
        # TODO: Calculate P(Class) and P(Feature|Class) for each feature
        pass

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Dự đoán nhãn cho các mẫu"""
        # TODO: Use Bayes rule to predict
        pass

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """Trả về xác suất dự đoán"""
        # TODO: Return probability for each class
        pass


def bayesian_inference(prior: float, likelihood: float, evidence: float) -> float:
    """
    Bayes Theorem: P(H|E) = P(E|H) * P(H) / P(E)
    - prior: P(Hypothesis)
    - likelihood: P(Evidence | Hypothesis)
    - evidence: P(Evidence)
    """
    if evidence == 0:
        return 0.0
    return (likelihood * prior) / evidence


class VariableElimination:
    """Variable Elimination algorithm for inference"""

    def __init__(self, network: BayesianNetwork):
        self.network = network

    def eliminate(self, query_var: str, evidence: Dict[str, str]) -> Dict[str, float]:
        """
        Variable Elimination
        """
        # TODO: Implement VE algorithm
        pass
