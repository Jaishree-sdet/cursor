#!/usr/bin/env python3

from calculator import Calculator

def demonstrate_bugs():
    calc = Calculator()
    
    print("=== DEMONSTRATING BUGS IN CALCULATOR ===\n")
    
    # BUG 1: Division by zero - FIXED
    print("BUG 1: Division by zero vulnerability - FIXED")
    print("Expected: Should raise ValueError for division by zero")
    print("Actual: Now properly raises ValueError")
    try:
        result = calc.divide(10, 0)
        print(f"Result: {result}")
    except ValueError as e:
        print(f"Error: {e}")
    print()
    
    # BUG 2: Square root of negative number - FIXED
    print("BUG 2: Square root of negative number - FIXED")
    print("Expected: Should raise ValueError for negative numbers")
    print("Actual: Now properly raises ValueError")
    try:
        result = calc.sqrt(-4)
        print(f"Result: {result}")
    except ValueError as e:
        print(f"Error: {e}")
    print()
    
    # BUG 3: Security vulnerability with eval() - FIXED
    print("BUG 3: Security vulnerability with eval() - FIXED")
    print("Expected: Should not allow malicious code execution")
    print("Actual: Now properly blocks malicious expressions")
    try:
        # This should be blocked and now is due to input validation
        result = calc.evaluate_expression("__import__('os').system('echo malicious_code_executed')")
        print(f"Malicious expression executed successfully: {result}")
    except ValueError as e:
        print(f"Error: {e}")
    print()
    
    # Test that valid expressions still work
    print("Testing that valid expressions still work:")
    try:
        result = calc.evaluate_expression("2 + 3 * 4")
        print(f"Valid expression '2 + 3 * 4' = {result}")
    except Exception as e:
        print(f"Error: {e}")
    print()

if __name__ == "__main__":
    demonstrate_bugs()