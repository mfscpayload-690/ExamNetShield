# utils.py
"""Utility functions for the ExamNetShield application."""

import os
from werkzeug.utils import secure_filename
from config import Config


def allowed_file(filename):
    """
    Check if the uploaded file has an allowed extension.
    
    Args:
        filename (str): The name of the file to check
        
    Returns:
        bool: True if file extension is allowed, False otherwise
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS


def secure_file_upload(file, upload_folder):
    """
    Securely handle file upload.
    
    Args:
        file: The file object from request.files
        upload_folder (str): The directory to save the file
        
    Returns:
        tuple: (success: bool, file_path: str or None, error_message: str or None)
    """
    if not file or file.filename == '':
        return False, None, 'No file selected'
    
    if not allowed_file(file.filename):
        return False, None, 'File type not allowed'
    
    # Secure the filename
    filename = secure_filename(file.filename)
    
    # Ensure upload folder exists
    os.makedirs(upload_folder, exist_ok=True)
    
    # Create file path
    file_path = os.path.join(upload_folder, filename)
    
    try:
        file.save(file_path)
        return True, file_path, None
    except Exception as e:
        return False, None, f'Error saving file: {str(e)}'


def validate_registration_range(reg_range):
    """
    Validate registration number range format.
    
    Args:
        reg_range (str): Range in format 'start-end'
        
    Returns:
        tuple: (success: bool, start: int or None, end: int or None, error: str or None)
    """
    try:
        start, end = map(int, reg_range.split('-'))
        if start >= end:
            return False, None, None, 'Range start must be less than end'
        if start < 0 or end < 0:
            return False, None, None, 'Range values must be positive'
        if end - start > 1000:
            return False, None, None, 'Range too large (max 1000 students)'
        return True, start, end, None
    except ValueError:
        return False, None, None, 'Invalid range format. Use start-end (e.g., 1-10)'
