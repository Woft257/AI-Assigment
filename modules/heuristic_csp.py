"""
(B) Heuristic & CSP - Heuristic và bài toán thỏa mãn ràng buộc
Các thuật toán: Hill Climbing, Genetic Algorithm, Backtracking CSP
"""

from typing import List, Dict, Any, Optional, Callable
import random


def hill_climbing(
    problem: Any,
    heuristic: Callable,
    max_iterations: int = 1000
) -> Optional[Any]:
    """
    Hill Climbing algorithm
    - problem: đối tượng bài toán với các method get_neighbors(), get_value()
    - heuristic: hàm đánh giá (càng nhỏ càng tốt)
    """
    # TODO: Implement Hill Climbing
    pass


def simulated_annealing(
    problem: Any,
    heuristic: Callable,
    schedule: Callable = None
) -> Optional[Any]:
    """
    Simulated Annealing algorithm
    """
    # TODO: Implement Simulated Annealing
    pass


class CSP:
    """
    Constraint Satisfaction Problem framework
    """

    def __init__(self, variables: List, domains: Dict, constraints: List):
        """
        - variables: danh sách các biến
        - domains: dict {var: [các giá trị có thể]}
        - constraints: list các hàm kiểm tra ràng buộc
        """
        self.variables = variables
        self.domains = domains
        self.constraints = constraints

    def backtracking_search(self, assignment: Dict = None) -> Optional[Dict]:
        """
        Backtracking CSP solver
        """
        # TODO: Implement Backtracking Search
        pass

    def AC3(self) -> bool:
        """
        Arc Consistency Algorithm 3 (AC-3)
        """
        # TODO: Implement AC-3
        pass


def genetic_algorithm(
    population: List,
    fitness: Callable,
    mutation: Callable,
    crossover: Callable,
    generations: int = 100,
    crossover_rate: float = 0.8,
    mutation_rate: float = 0.1
) -> Any:
    """
    Genetic Algorithm
    """
    # TODO: Implement GA
    pass
