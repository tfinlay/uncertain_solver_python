# uncertain_solver_python
An implementation of an uncertainty-aware calculator in python. A dart version is available [here](https://github.com/tfinlay/uncertain_solver)

## Overview


This module provides four classes, all derived from a general `EquationComponent` which represents a numerical value and its associated uncertainty.
1. EquationValue, which represents a measured value.
2. EquationBrackets, which essentially stands in for a bracket in a real mathematical formula, grouping equation components and applying an operator to them all. Available operations are: add, subtract, multiply, and divide.
3. EquationPower, which represents an EquationComponent to the power of a positive integer value.
4. EquationFunction, which allows the use of complex mathematical functions to be performed on its EquationComponent. It calculates uncertainty using the Brute Force method.

NOTE: Some modification may be required to account for differences in methodology.

## Usage Example

A simple usage example, for calculating the mass of the energy converted from gravitational energy when a (10000000000000000 ± 10000000) kg mass is dropped (5 ± 0.1) metres.

Rearranging the equations: `E = m_2 * c^2` and `E = m_1 * g * h`, gives: `m_2 = (m_1 * g * h) / (c^2)`

```python
from decimal import Decimal as D
from uncertain_solver import *

# define values
m_1 = EquationValue.from_uncertainty_plus_minus(D("10000000000000000"), uncertainty_plus_minus=D("10000000"))
g = EquationValue(D('9.7988'), uncertainty_percentage=D("0.7"))  # From: https://physics.stackexchange.com/a/93298
h = EquationValue.from_uncertainty_plus_minus(D('5'), uncertainty_plus_minus=D('0.1'))
c = EquationValue(D('299792458'), uncertainty_percentage=D('0'))

# Define equation
m_2 = EquationBrackets(
    [
        EquationBrackets([m_1, g, h], operator=EquationOperator.MULTIPLY),
        EquationPower(c, power=2)
    ],
    operator=EquationOperator.DIVIDE
)

print(m_2)
```

For a complete demonstration, see `example.py`.