# pylint: disable=missing-docstring

from logiclib.formula import Formula
from logiclib.parser import parse_formula


def main():
    formula: Formula
    formula, = parse_formula("∀x(P(x) → ¬Q(x))")
    print(formula)


if __name__ == "__main__":
    main()
