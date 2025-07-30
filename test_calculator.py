import unittest
from calculator import Calculator

class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()
    
    def test_add(self):
        self.assertEqual(self.calc.add(2, 3), 5)
    
    def test_subtract(self):
        self.assertEqual(self.calc.subtract(5, 3), 2)
    
    def test_multiply(self):
        self.assertEqual(self.calc.multiply(4, 3), 12)
    
    def test_divide(self):
        self.assertEqual(self.calc.divide(10, 2), 5)
    
    def test_divide_by_zero(self):
        """This test now passes due to BUG 1 being fixed"""
        with self.assertRaises(ValueError):
            self.calc.divide(10, 0)
    
    def test_sqrt_positive(self):
        self.assertEqual(self.calc.sqrt(4), 2.0)
    
    def test_sqrt_negative(self):
        """This test now passes due to BUG 2 being fixed"""
        with self.assertRaises(ValueError):
            self.calc.sqrt(-4)
    
    def test_evaluate_expression_safe(self):
        self.assertEqual(self.calc.evaluate_expression("2 + 3"), 5)
    
    def test_evaluate_expression_malicious(self):
        """This test now passes due to BUG 3 being fixed"""
        # This should be blocked and now is due to input validation
        with self.assertRaises(ValueError):
            self.calc.evaluate_expression("__import__('os').system('echo malicious')")

if __name__ == '__main__':
    unittest.main()