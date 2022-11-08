"""
This module provides utilities to parse strings into formula objects.
"""

from typing import List
from pyparsing import (
    Char, OpAssoc, Word, alphas, alphanums, delimited_list, infix_notation,
    one_of
)
from logiclib.formula import (
    Formula, Predicate, Universal, Existential, Negation, Conjunction,
    Disjunction, Implication, BiImplication
)


def predicate_action(_s, _loc, toks: List[str]) -> Predicate:
    """
    Parse action for predicate.
    """
    name: str
    variables: List[str]
    name, variables = toks
    return Predicate(name, variables)


def universal_action(toks: List[str]) -> Universal:
    """
    Parse action for universal quantifier.
    """
    return Universal(*toks[0])


def existential_action(toks: List[str]) -> Existential:
    """
    Parse action for existential quantifier.
    """
    return Existential(*toks[0])


var_name_element = Word(alphas, alphanums)
predicate_element = (
    var_name_element
    + Char("(").suppress()
    + delimited_list(var_name_element)
    + Char(")").suppress()
)
universal_element = (
    (one_of(Universal.symbol + " !")
     | one_of(r"forall \forall", as_keyword=True)).suppress()
    + var_name_element
)
existential_element = (
    (one_of(Existential.symbol + "?")
     | one_of(r"exist exists \exist \exists", as_keyword=True)).suppress()
    + var_name_element
)
negation_element = (
    one_of(Negation.symbol + " ~")
    | one_of(r"not \lnot", as_keyword=True)).suppress()
conjunction_element = (
    one_of(Conjunction.symbol + " &")
    | one_of(r"and \land", as_keyword=True)).suppress()
disjunction_element = (
    one_of(Disjunction.symbol + " |")
    | one_of(r"or \lor", as_keyword=True)).suppress()
implication_element = (
    one_of(Implication.symbol + " ->")
    | one_of(r"implies to \implies \to", as_keyword=True)).suppress()
bi_implication_element = (
    one_of(BiImplication.symbol + " <->")
    | one_of(r"\leftrightarrow", as_keyword=True)).suppress()
formula_element = infix_notation(
    predicate_element.add_parse_action(predicate_action),
    [
        (universal_element, 1, OpAssoc.RIGHT, universal_action),
        (existential_element, 1, OpAssoc.RIGHT, existential_action),
        (negation_element, 1, OpAssoc.RIGHT, lambda toks: Negation(*toks[0])),
        (conjunction_element, 2,
         OpAssoc.LEFT , lambda toks: Conjunction(*toks[0])),
        (disjunction_element, 2,
         OpAssoc.LEFT , lambda toks: Disjunction(*toks[0])),
        (implication_element, 2,
         OpAssoc.RIGHT, lambda toks: Implication(*toks[0])),
        (bi_implication_element, 2,
         OpAssoc.RIGHT, lambda toks: BiImplication(*toks[0]))
    ]
)


def parse_formula(instring) -> List[Formula]:
    """
    Parse instring into a Formula object.
    """
    return formula_element.parse_string(instring, parse_all=True)
