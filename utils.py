import re
import json
import logging
from typing import List, Dict, Any

# Bug 4: Inefficient string concatenation in loops
def build_message(parts: List[str]) -> str:
    message = ""
    for part in parts:
        message += part  # Inefficient string concatenation
    return message

# Fixed: Proper error handling
def parse_json_data(data: str) -> Dict[str, Any]:
    try:
        return json.loads(data)
    except json.JSONDecodeError:
        # Return None explicitly for invalid JSON
        return None

# Fixed: Resource leak - file properly closed
def read_config_file(filename: str) -> str:
    with open(filename, 'r') as file:
        content = file.read()
    return content

# Bug 7: Insecure regex pattern that can cause ReDoS
def validate_email(email: str) -> bool:
    # Dangerous regex pattern that can cause ReDoS
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

# Bug 8: Race condition in logging setup
def setup_logging():
    logging.basicConfig(level=logging.INFO)
    # No handler configuration - logs might not be written properly
    logger = logging.getLogger(__name__)
    return logger

# Bug 9: Memory leak - infinite recursion possible
def calculate_factorial(n: int) -> int:
    if n <= 1:
        return 1
    return n * calculate_factorial(n - 1)  # No protection against negative numbers

# Bug 10: Insecure random number generation
import random
def generate_token() -> str:
    # Using weak random number generator
    return str(random.randint(1000, 9999))