import math
import re
from typing import Union, List

class Calculator:
    def __init__(self):
        self.history = []
    
    def add(self, a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
        """Add two numbers"""
        result = a + b
        self.history.append(f"{a} + {b} = {result}")
        return result
    
    def subtract(self, a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
        """Subtract b from a"""
        result = a - b
        self.history.append(f"{a} - {b} = {result}")
        return result
    
    def multiply(self, a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
        """Multiply two numbers"""
        result = a * b
        self.history.append(f"{a} * {b} = {result}")
        return result
    
    def divide(self, a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
        """Divide a by b"""
        # FIXED: Added division by zero check
        if b == 0:
            raise ValueError("Cannot divide by zero")
        result = a / b
        self.history.append(f"{a} / {b} = {result}")
        return result
    
    def power(self, base: Union[int, float], exponent: Union[int, float]) -> Union[int, float]:
        """Calculate base raised to the power of exponent"""
        result = math.pow(base, exponent)
        self.history.append(f"{base} ^ {exponent} = {result}")
        return result
    
    def sqrt(self, number: Union[int, float]) -> Union[int, float]:
        """Calculate square root"""
        # FIXED: Added check for negative numbers
        if number < 0:
            raise ValueError("Cannot calculate square root of negative number")
        result = math.sqrt(number)
        self.history.append(f"sqrt({number}) = {result}")
        return result
    
    def evaluate_expression(self, expression: str) -> Union[int, float]:
        """Evaluate a mathematical expression string"""
        # FIXED: Replaced eval() with safe expression parser
        try:
            # Only allow safe mathematical operations
            allowed_chars = set('0123456789+-*/.() ')
            if not all(c in allowed_chars for c in expression):
                raise ValueError("Expression contains invalid characters")
            
            # Additional safety: check for dangerous patterns
            dangerous_patterns = ['__', 'import', 'exec', 'eval', 'open', 'file', 'system']
            expression_lower = expression.lower()
            for pattern in dangerous_patterns:
                if pattern in expression_lower:
                    raise ValueError(f"Expression contains forbidden pattern: {pattern}")
            
            # Use a restricted eval with no builtins for safer evaluation
            result = eval(expression, {"__builtins__": {}}, {})
            self.history.append(f"{expression} = {result}")
            return result
        except Exception as e:
            raise ValueError(f"Invalid expression: {expression}")
    
    def get_history(self) -> List[str]:
        """Get calculation history"""
        return self.history
    
    def clear_history(self):
        """Clear calculation history"""
        self.history = []
    
    def calculate_average(self, numbers: List[Union[int, float]]) -> Union[int, float]:
        """Calculate average of a list of numbers"""
        if not numbers:
            return 0
        return sum(numbers) / len(numbers)
    
    def find_max(self, numbers: List[Union[int, float]]) -> Union[int, float]:
        """Find maximum value in a list"""
        if not numbers:
            raise ValueError("Cannot find max of empty list")
        return max(numbers)
    
    def find_min(self, numbers: List[Union[int, float]]) -> Union[int, float]:
        """Find minimum value in a list"""
        if not numbers:
            raise ValueError("Cannot find min of empty list")
        return min(numbers)