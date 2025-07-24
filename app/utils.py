# TODO: Implement utility functions here
# Consider functions for:
# - Generating short codes
# - Validating URLs
# - Any other helper functions you need
# app/utils.py

import random
import string

def generate_short_code(length=6):
    """Generates a random short code of a given length."""
    # 6 alphanumeric characters.
    characters = string.ascii_letters + string.digits
    return "".join(random.choices(characters, k=length))

def validate_url(url):
    """A simple check to validate a URL."""
    # This is a basic check. For a real-world app, you might use a more
    # robust library or a complex regular expression.
    return url.startswith("http://") or url.startswith("https://")