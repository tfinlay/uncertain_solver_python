from decimal import Decimal


def sqrt(value: Decimal) -> Decimal:
    return value.sqrt()


def pow(value: Decimal, power: Decimal) -> Decimal:
    """value to the given power."""
    return value ** power


def exp(value: Decimal) -> Decimal:
    """e to the power of value"""
    return value.exp()


def log(value: Decimal, base: Decimal) -> Decimal:
    return value.log10() / base.log10()


def ln(value: Decimal) -> Decimal:
    return value.ln()


def log10(value: Decimal) -> Decimal:
    return value.log10()


def logb(value: Decimal) -> Decimal:
    return value.logb()
