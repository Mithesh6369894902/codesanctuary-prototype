def add_numbers(a, b):
    """Add two numbers safely."""
    try:
        return a + b
    except TypeError:
        return float(a) + float(b)

def factorial(n):
    """Compute factorial recursively."""
    if n <= 1:
        return 1
    return n * factorial(n - 1)
