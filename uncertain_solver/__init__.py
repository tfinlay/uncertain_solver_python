from decimal import Decimal
from typing import Callable, Optional
from .util import *


class EquationComponent:
    @property
    def value(self) -> Decimal:
        raise NotImplementedError()

    @property
    def uncertainty_percentage(self) -> Decimal:
        raise NotImplementedError()

    @property
    def uncertainty_plus_minus(self) -> Decimal:
        return self.value * self.uncertainty_percentage

    def does_intersect_with(self, other):
        if other.value <= self.value and (other.value + other.uncertainty_plus_minus) >= (self.value - self.uncertainty_plus_minus):
            return True
        elif other.value > self.value and (other.value - other.uncertainty_plus_minus) <= (self.value + self.uncertainty_plus_minus):
            return True
        return False

    def __repr__(self):
        return f"<{type(self).__name__} {self.value} ± {self.uncertainty_plus_minus} (%𝛿 = {self.uncertainty_percentage})"


class EquationValue (EquationComponent):
    def __init__(self, value: Decimal, uncertainty_percentage: Decimal):
        self._value = value
        self._uncertainty_percentage = uncertainty_percentage

    @classmethod
    def from_uncertainty_plus_minus(cls, value: Decimal, uncertainty_plus_minus: Decimal):
        return cls(
            value=value,
            uncertainty_percentage=uncertainty_plus_minus / value
        )

    @property
    def value(self):
        return self._value

    @property
    def uncertainty_percentage(self):
        return self._uncertainty_percentage


class EquationBrackets (EquationComponent):
    def __init__(self, values: [EquationComponent], operator: EquationOperator):
        self._values = values
        self._operator = operator

    @property
    def value(self):
        return apply_operator_to_get_value(self._operator, list(map(lambda e: e.value, self._values)))

    @property
    def uncertainty_percentage(self):
        return apply_operator_to_get_uncertainty_percentage(self._operator, self._values)


class EquationPower (EquationComponent):
    """
    Although this can be done with an EquationFunction component, this way minimises errors when working with positive integer powers.
    """
    def __init__(self, argument: EquationComponent, power: int):
        self._brackets = EquationBrackets(
            [argument for _ in range(power)],
            operator=EquationOperator.MULTIPLY
        )

    @property
    def value(self):
        return self._brackets.value

    @property
    def uncertainty_percentage(self):
        return self._brackets.uncertainty_percentage

    @property
    def uncertainty_plus_minus(self):
        return self._brackets.uncertainty_plus_minus


class EquationFunction (EquationComponent):
    """
    A generic EquationComponent that adds function support (e.g. sin, cos, tan, sqrt, ...)
    """
    def __init__(self, function: Callable[[Decimal, Optional[Decimal]], Decimal], primary_argument: EquationComponent, secondary_arguments: Optional[list] = tuple()):
        self._function = function
        self._primary_argument = primary_argument
        self._secondary_arguments = secondary_arguments

    @property
    def value(self) -> Decimal:
        return self._function(self._primary_argument.value, *self._secondary_arguments)

    @property
    def uncertainty_plus_minus(self) -> Decimal:
        return self._function(
            self._primary_argument.value + self._primary_argument.uncertainty_plus_minus,
            *self._secondary_arguments
        ) - self._function(self._primary_argument.value, *self._secondary_arguments)

    @property
    def uncertainty_percentage(self) -> Decimal:
        return self.uncertainty_plus_minus / self.value
