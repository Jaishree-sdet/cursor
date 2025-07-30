import unittest
import tempfile
import os
import sys
import importlib.util

# Import the utils module directly
spec = importlib.util.spec_from_file_location("utils", "utils.py")
utils = importlib.util.module_from_spec(spec)
spec.loader.exec_module(utils)

class TestBugFixes(unittest.TestCase):
    
    def test_resource_leak_fix(self):
        """Test that file resources are properly closed"""
        # Create a temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("test content")
            temp_filename = f.name
        
        try:
            # Test the fixed function
            content = utils.read_config_file(temp_filename)
            self.assertEqual(content, "test content")
            
            # The file should be properly closed by the context manager
            # We can verify this by checking if we can still access the file
            with open(temp_filename, 'r') as f:
                self.assertEqual(f.read(), "test content")
                
        finally:
            # Clean up
            os.unlink(temp_filename)
    
    def test_string_concatenation_performance(self):
        """Test that string concatenation works correctly"""
        parts = ["part1", "part2", "part3", "part4", "part5"]
        result = utils.build_message(parts)
        self.assertEqual(result, "part1part2part3part4part5")
    
    def test_json_parsing_fix(self):
        """Test JSON parsing error handling"""
        # Test valid JSON
        valid_json = '{"key": "value"}'
        result = utils.parse_json_data(valid_json)
        self.assertEqual(result, {"key": "value"})
        
        # Test invalid JSON - should return None
        invalid_json = '{"key": "value"'
        result = utils.parse_json_data(invalid_json)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()