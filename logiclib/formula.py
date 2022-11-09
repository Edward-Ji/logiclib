"""
This module contains abstractions of formulas.
"""

from abc import ABC, abstractmethod
from itertools import zip_longest
from dataclasses import dataclass
from typing import ClassVar, Dict, List, Set


class Formula(ABC):

    def __invert__(self):
        return Negation(self)

    def __and__(self, other):
        if not isinstance(other, Formula):
            raise TypeError("unsupported operand type(s)")
        return Conjunction(self, other)

    def __or__(self, other):
        if not isinstance(other, Formula):
            raise TypeError("unsupported operand type(s)")
        return Disjunction(self, other)

    @abstractmethod
    def rename_var(self, var_map: Dict[str, str]):
        pass

    @abstractmethod
    def same_as(self, other: "Formula", var_map: Dict[str, str] = None) -> bool:
        pass

    @abstractmethod
    def get_free_vars(self) -> Set[str]:
        pass


@dataclass
class Predicate(Formula):
    name: str
    variables: List[str]

    def __str__(self):
        vars_str: str = ",".join(self.variables)
        return f"{self.name}({vars_str})"

    def rename_var(self, var_map: Dict[str, str]):
        self.variables = [var_map.get(var, var) for var in self.variables]

    def same_as(self, other: Formula, var_map: Dict[str, str] = None) -> bool:
        if type(other) is not type(other):
            return False
        if self.name != other.name:
            return False
        if var_map is None:
            var_map = {}
        for self_var, other_var in zip_longest(self.variables, other.variables):
            if var_map.get(self_var, self_var) != other_var:
                return False

        return True

    def get_free_vars(self) -> Set[str]:
        return set(self.variables)


@dataclass
class Operator(Formula):
    symbol: ClassVar[str]


@dataclass
class Unary(Operator):
    right: Formula

    def __str__(self):
        return f"{self.symbol}{self.right}"

    def rename_var(self, var_map: Dict[str, str]):
        self.right.rename_var(var_map)

    def same_as(self, other: Formula, var_map: Dict[str, str] = None) -> bool:
        if type(self) is not type(other):
            return False
        return self.right.same_as(other.right, var_map)

    def get_free_vars(self) -> Set[str]:
        return self.right.get_free_vars()


@dataclass
class Binary(Operator):
    left: Formula
    right: Formula

    def __str__(self):
        return f"({self.left}{self.symbol}{self.right})"

    def rename_var(self, var_map: Dict[str, str]):
        self.left.rename_var(var_map)
        self.right.rename_var(var_map)

    def same_as(self, other: Formula, var_map: Dict[str, str] = None) -> bool:
        if type(self) is not type(other):
            return False
        return (self.left.same_as(other.left, var_map)
                and self.right.same_as(other.right, var_map))

    def get_free_vars(self) -> Set[str]:
        return self.left.get_free_vars().union(self.right.get_free_vars())


@dataclass
class Quantifier(Operator):
    var: str
    right: Formula

    def __str__(self):
        return f"{self.symbol}{self.var}{self.right}"

    def rename_var(self, var_map: Dict[str, str]):
        self.var = var_map.get(self.var, self.var)
        self.right.rename_var(var_map)

    def same_as(self, other: Formula, var_map: Dict[str, str] = None) -> bool:
        if type(self) is not type(other):
            return False
        if var_map is None:
            var_map = {}
        var_map = var_map | {self.var: other.var}
        return self.right.same_as(other.right, var_map)

    def get_free_vars(self) -> Set[str]:
        return self.right.get_free_vars().difference({self.var})


@dataclass
class Negation(Unary):
    symbol: ClassVar[str] = "¬"


@dataclass
class Universal(Quantifier):
    symbol: ClassVar[str] = "∀"


@dataclass
class Existential(Quantifier):
    symbol: ClassVar[str] = "∃"


@dataclass
class Conjunction(Binary):
    symbol: ClassVar[str] = "∧"


@dataclass
class Disjunction(Binary):
    symbol: ClassVar[str] = "∨"


@dataclass
class Implication(Binary):
    symbol: ClassVar[str] = "→"


@dataclass
class BiImplication(Binary):
    symbol: ClassVar[str] = "↔"
