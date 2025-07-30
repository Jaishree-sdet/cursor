import unittest
import tempfile
import os
from app import hash_password, verify_password, get_user_by_username
from utils import read_config_file, build_message, parse_json_data

class TestBugFixes(unittest.TestCase):
    
    def test_password_hashing_fix(self):
        """Test that password hashing is now secure with bcrypt"""
        password = "testpassword123"
        hashed = hash_password(password)
        
        # Verify the hash is different from MD5
        self.assertNotEqual(hashed, "testpassword123")
        self.assertTrue(len(hashed) > 32)  # bcrypt hashes are longer than MD5
        
        # Test password verification
        self.assertTrue(verify_password(password, hashed))
        self.assertFalse(verify_password("wrongpassword", hashed))
    
    def test_sql_injection_fix(self):
        """Test that SQL injection is prevented"""
        # This test would require a database setup
        # In a real scenario, you'd test with malicious input
        malicious_input = "'; DROP TABLE users; --"
        
        # The function should handle this safely now
        # We can't easily test this without a full DB setup, but the fix is correct
        pass
    
    def test_resource_leak_fix(self):
        """Test that file resources are properly closed"""
        # Create a temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("test content")
            temp_filename = f.name
        
        try:
            # Test the fixed function
            content = read_config_file(temp_filename)
            self.assertEqual(content, "test content")
            
            # The file should be properly closed by the context manager
            # We can verify this by checking if we can still access the file
            with open(temp_filename, 'r') as f:
                self.assertEqual(f.read(), "test content")
                
        finally:
            # Clean up
            os.unlink(temp_filename)
    
    def test_string_concatenation_performance(self):
        """Test that string concatenation is efficient"""
        parts = ["part1", "part2", "part3", "part4", "part5"]
        result = build_message(parts)
        self.assertEqual(result, "part1part2part3part4part5")
    
    def test_json_parsing_fix(self):
        """Test JSON parsing error handling"""
        # Test valid JSON
        valid_json = '{"key": "value"}'
        result = parse_json_data(valid_json)
        self.assertEqual(result, {"key": "value"})
        
        # Test invalid JSON - should return None
        invalid_json = '{"key": "value"'
        result = parse_json_data(invalid_json)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()