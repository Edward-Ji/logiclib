"""
This module contains abstractions of formulas.
"""

from dataclasses import dataclass
from typing import ClassVar, List


class Formula:

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


@dataclass
class Predicate(Formula):
    name: str
    variables: List[str]

    def __str__(self):
        vars_str: str = ",".join(self.variables)
        return f"{self.name}({vars_str})"


@dataclass
class Operator(Formula):
    symbol: ClassVar[str]


@dataclass
class Unary(Operator):
    right: Formula

    def __str__(self):
        return f"{self.symbol}{self.right}"


@dataclass
class Binary(Operator):
    left: Formula
    right: Formula

    def __str__(self):
        return f"({self.left}{self.symbol}{self.right})"


@dataclass
class Quantifier(Operator):
    var: str
    right: Formula

    def __str__(self):
        return f"{self.symbol}{self.var}{self.right}"


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
