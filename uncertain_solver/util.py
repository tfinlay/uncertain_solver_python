from decimal import Decimal
from enum import Enum
from functools import reduce


class EquationOperator (Enum):
    ADD = 0
    SUBTRACT = 1
    MULTIPLY = 2
    DIVIDE = 3


def apply_operator_to_get_value(operator: EquationOperator, values: [Decimal]) -> Decimal:
    if operator is EquationOperator.ADD:
        return sum(values)
    elif operator is EquationOperator.SUBTRACT:
        if len(values) != 2:
            raise ValueError("A subtraction can only occur between exactly 2 values.")
        return values[0] - values[1]
    elif operator is EquationOperator.MULTIPLY:
        return reduce(lambda prod_so_far, value: prod_so_far * value, values, Decimal(1))
    elif operator is EquationOperator.DIVIDE:
        if len(values) != 2:
            raise ValueError("A division can only occur between exactly 2 values.")
        return values[0] / values[1]

    raise ValueError("Unrecognised operator.")


def apply_operator_to_get_uncertainty_percentage(operator: EquationOperator, values) -> Decimal:
    if operator is EquationOperator.MULTIPLY or operator is EquationOperator.DIVIDE:
        return sum(map(lambda e: e.uncertainty_percentage, values))
    elif operator is EquationOperator.ADD or operator is EquationOperator.SUBTRACT:
        return sum(map(lambda e: e.uncertainty_plus_minus, values)) / sum(map(lambda e: e.value, values))

    raise ValueError("Unrecognised operator.")