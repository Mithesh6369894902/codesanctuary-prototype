def reverse_string(s: str) -> str:
    """Return the reversed version of a string."""
    return s[::-1]

def is_palindrome(s: str) -> bool:
    """Check if a string reads the same backwards."""
    s = s.lower().replace(" ", "")
    return s == s[::-1]
