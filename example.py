"""
Calculating the magnitude of a line from (0, 0, 0) to (1 ± 0.01, 50 ± 10, 16.9 ± 2.3)
||(a, b, c)|| = sqrt(a**2 + b**2 + c**2)
"""
from decimal import Decimal as D
from uncertain_solver import *
from uncertain_solver.functions import sqrt

a = EquationValue.from_uncertainty_plus_minus(D("1"), uncertainty_plus_minus=D("0.01"))
b = EquationValue.from_uncertainty_plus_minus(D("-50"), uncertainty_plus_minus=D("10"))
c = EquationValue.from_uncertainty_plus_minus(D("16.9"), uncertainty_plus_minus=D("2.3"))

magnitude = EquationFunction(
    sqrt,
    EquationBrackets(
        [
            EquationPower(a, power=2),
            EquationPower(b, power=2),
            EquationPower(c, power=2)
        ],
        operator=EquationOperator.ADD
    )
)

print(magnitude)

"""
Generalisation.

Since it's just python code, this calculation can be generalised like so:
Calculating the magnitude of a line from (a, b, c) to (d, e, f) where every measurement has the same uncertainty.
||(a,b,c) - (d,e,f)|| = ||(a-d, b-e, c-f)|| = sqrt((a-d)**2 + (b-e)**2 + (c-f)**2)
"""


def uncertain_magnitude(a: Decimal, b: Decimal, c: Decimal, d: Decimal, e: Decimal, f: Decimal,
                        uncertainty: Decimal) -> (Decimal, Decimal):
    """
    Calculates the magnitude of the line between (a,b,c) and (d,e,f) where each value has an uncertainty of ±<uncertainty>
    :return: tuple<Decimal, Decimal>, the distance and its uncertainty
    """
    a_value = EquationValue.from_uncertainty_plus_minus(a, uncertainty_plus_minus=uncertainty)
    b_value = EquationValue.from_uncertainty_plus_minus(b, uncertainty_plus_minus=uncertainty)
    c_value = EquationValue.from_uncertainty_plus_minus(c, uncertainty_plus_minus=uncertainty)
    d_value = EquationValue.from_uncertainty_plus_minus(d, uncertainty_plus_minus=uncertainty)
    e_value = EquationValue.from_uncertainty_plus_minus(e, uncertainty_plus_minus=uncertainty)
    f_value = EquationValue.from_uncertainty_plus_minus(f, uncertainty_plus_minus=uncertainty)

    mag = EquationFunction(
        sqrt,
        EquationBrackets(
            [
                EquationPower(
                    EquationBrackets([a_value, d_value], operator=EquationOperator.SUBTRACT),
                    power=2
                ),
                EquationPower(
                    EquationBrackets([b_value, e_value], operator=EquationOperator.SUBTRACT),
                    power=2
                ),
                EquationPower(
                    EquationBrackets([c_value, f_value], operator=EquationOperator.SUBTRACT),
                    power=2
                )
            ],
            operator=EquationOperator.ADD
        )
    )

    return mag.value, mag.uncertainty_plus_minus


print(uncertain_magnitude(
    D("1"), D("1"), D("1"),
    D("2"), D("2"), D("2"),
    uncertainty=D("0.001")
))
