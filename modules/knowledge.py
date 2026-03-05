"""
(C) Knowledge Representation & Reasoning - Biểu diễn và suy luận tri thức
Các phương pháp: Propositional Logic, First-Order Logic, IF-THEN Rules
"""

from typing import List, Dict, Set, Any, Optional


class Proposition:
    """Mệnh đề logic"""

    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return isinstance(other, Proposition) and self.name == other.name

    def __hash__(self):
        return hash(self.name)


class KB:
    """Knowledge Base - Cơ sở tri thức"""

    def __init__(self):
        self.facts: Set[Proposition] = set()
        self.rules: List['Rule'] = []

    def add_fact(self, fact: Proposition):
        """Thêm sự kiện"""
        self.facts.add(fact)

    def add_rule(self, rule: 'Rule'):
        """Thêm luật"""
        self.rules.append(rule)

    def ask(self, query: Proposition) -> bool:
        """Hỏi - Forward chaining"""
        # TODO: Implement forward chaining
        pass


class Rule:
    """Luật IF-THEN"""

    def __init__(self, antecedents: List[Proposition], consequent: Proposition):
        """
        - antecedents: danh sách điều kiện (AND)
        - consequent: kết luận
        """
        self.antecedents = antecedents
        self.consequent = consequent

    def __repr__(self):
        ant = " AND ".join(str(a) for a in self.antecedents)
        return f"IF {ant} THEN {self.consequent}"


def forward_chaining(kb: KB, query: Proposition) -> bool:
    """
    Thuật toán suy luận tiến (Forward Chaining)
    """
    # TODO: Implement forward chaining
    pass


def backward_chaining(kb: KB, query: Proposition) -> bool:
    """
    Thuật toán suy luận lùi (Backward Chaining)
    """
    # TODO: Implement backward chaining
    pass


class LogicParser:
    """Parser cho logic mệnh đề"""

    SYMBOLS = {'AND', 'OR', 'NOT', 'IMPLIES', '('}

    def __init__(self):
        self.variables: Set[str] = set()

    def parse(self, expression: str) -> Any:
        """Parse biểu thức logic"""
        # TODO: Implement parser
        pass

    def evaluate(self, expression: Any, assignment: Dict[str, bool]) -> bool:
        """Đánh giá biểu thức với assignment"""
        # TODO: Implement evaluation
        pass


def resolution(kb: KB, query: Proposition) -> bool:
    """
    Suy luận bằng phương pháp Resolution
    """
    # TODO: Implement resolution
    pass
