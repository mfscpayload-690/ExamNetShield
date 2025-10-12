"""Test utility functions."""
import pytest
from utils import allowed_file, validate_registration_range


class TestAllowedFile:
    """Test the allowed_file function."""
    
    def test_allowed_extensions(self):
        """Test that allowed file extensions return True."""
        assert allowed_file('document.pdf') == True
        assert allowed_file('image.png') == True
        assert allowed_file('code.py') == True
        assert allowed_file('archive.zip') == True
        
    def test_disallowed_extensions(self):
        """Test that disallowed file extensions return False."""
        assert allowed_file('malware.exe') == False
        assert allowed_file('script.sh') == False
        assert allowed_file('file.xyz') == False
        
    def test_no_extension(self):
        """Test files without extensions."""
        assert allowed_file('noextension') == False
        
    def test_multiple_dots(self):
        """Test files with multiple dots."""
        assert allowed_file('file.backup.txt') == True
        assert allowed_file('archive.tar.gz') == False


class TestValidateRegistrationRange:
    """Test the validate_registration_range function."""
    
    def test_valid_range(self):
        """Test valid registration ranges."""
        success, start, end, error = validate_registration_range('1-10')
        assert success == True
        assert start == 1
        assert end == 10
        assert error is None
        
    def test_start_equals_end(self):
        """Test when start equals end."""
        success, start, end, error = validate_registration_range('5-5')
        assert success == False
        assert 'start must be less than end' in error
        
    def test_start_greater_than_end(self):
        """Test when start is greater than end."""
        success, start, end, error = validate_registration_range('10-5')
        assert success == False
        assert 'start must be less than end' in error
        
    def test_negative_values(self):
        """Test negative values."""
        success, start, end, error = validate_registration_range('-5-10')
        assert success == False
        assert 'positive' in error
        
    def test_invalid_format(self):
        """Test invalid format."""
        success, start, end, error = validate_registration_range('1,10')
        assert success == False
        assert 'Invalid range format' in error
        
    def test_range_too_large(self):
        """Test range that's too large."""
        success, start, end, error = validate_registration_range('1-2000')
        assert success == False
        assert 'too large' in error
        
    def test_non_numeric(self):
        """Test non-numeric values."""
        success, start, end, error = validate_registration_range('a-b')
        assert success == False
        assert 'Invalid range format' in error
