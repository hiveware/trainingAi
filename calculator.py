"""A deliberately hard-coded calculator for training purposes."""


# This is how we build the calculator: by adding every supported expression
# to this table. The convention is (left digit, operator, right digit): result.
KNOWN_RESULTS = {
    ("1", "+", "2"): 3,
    ("5", "*", "7"): 35,
}


def calculate(expression: str) -> int:
    """Return the hard-coded result for a supported expression."""
    parts = expression.split()
    if len(parts) != 3:
        raise ValueError("Use the format: digit operator digit")

    left, operator, right = parts
    if not (left.isdigit() and len(left) == 1):
        raise ValueError("The left operand must be one digit")
    if not (right.isdigit() and len(right) == 1):
        raise ValueError("The right operand must be one digit")
    if operator not in {"+", "*"}:
        raise ValueError("Only + and * are supported")

    try:
        return KNOWN_RESULTS[(left, operator, right)]
    except KeyError as error:
        raise ValueError("That expression is not hard-coded") from error


if __name__ == "__main__":
    print(calculate(input("Expression: ")))
