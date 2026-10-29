"""Public membrane around the intentionally indirect lookup machinery."""

from labyrinth import ResolverFacade


_FACADE = ResolverFacade.bootstrap()


def calculate(expression: str) -> int:
    """Resolve an expression through the sealed hard-coded registry."""
    return _FACADE.resolve(expression)


if __name__ == "__main__":
    print(calculate(input("Expression: ")))
