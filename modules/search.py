"""
(A) Search Algorithms - Tìm kiếm
Các thuật toán: BFS, DFS, Uniform Cost, Best-first, A*
"""

from typing import List, Dict, Any, Optional
from collections import deque
import heapq


class Problem:
    """Base class cho bài toán tìm kiếm"""

    def __init__(self):
        self.initial_state = None
        self.goal_state = None

    def actions(self, state):
        """Trả về các action có thể thực hiện từ state"""
        raise NotImplementedError

    def result(self, state, action):
        """Trả về state mới sau khi thực hiện action"""
        raise NotImplementedError

    def goal_test(self, state):
        """Kiểm tra state có phải goal không"""
        raise NotImplementedError

    def path_cost(self, cost, state1, action, state2):
        """Tính chi phí đường đi"""
        raise NotImplementedError


class SearchNode:
    """Node trong cây tìm kiếm"""

    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def __lt__(self, other):
        return self.path_cost < other.path_cost


def bfs(problem: Problem) -> Optional[SearchNode]:
    """Breadth-First Search"""
    # TODO: Implement BFS
    pass


def dfs(problem: Problem, limit: int = 1000) -> Optional[SearchNode]:
    """Depth-First Search"""
    # TODO: Implement DFS
    pass


def uniform_cost_search(problem: Problem) -> Optional[SearchNode]:
    """Uniform Cost Search"""
    # TODO: Implement UCS
    pass


def best_first_search(problem: Problem, heuristic) -> Optional[SearchNode]:
    """Best-First Search"""
    # TODO: Implement Best-First
    pass


def a_star_search(problem: Problem, heuristic) -> Optional[SearchNode]:
    """A* Search"""
    # TODO: Implement A*
    pass


def reconstruct_path(node: SearchNode) -> List:
    """Tái tạo đường đi từ goal về start"""
    path = []
    while node.parent:
        path.append(node.action)
        node = node.parent
    return list(reversed(path))
