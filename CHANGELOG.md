# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Environment variable configuration via `.env` file
- Configuration management with `config.py`
- Utility functions for file upload and validation in `utils.py`
- Logout functionality for teachers
- Comprehensive logging throughout the application
- Unit tests with pytest
- Integration tests for authentication
- GitHub Actions CI/CD pipeline
- Docker and docker-compose support
- CONTRIBUTING.md with development guidelines
- SECURITY.md with security policy
- API.md with API documentation
- requirements-dev.txt for development dependencies
- Improved navigation bar with conditional display
- Username display in navbar
- Test fixtures and configuration

### Changed
- SECRET_KEY now loaded from environment variables (no longer regenerates on restart)
- Session management now uses secure cookies with configurable timeout
- File upload now uses secure validation and sanitization
- create_user.py now uses interactive password input (no hardcoded credentials)
- README.md updated with Docker setup and improved installation instructions
- Improved error handling with try-catch blocks throughout
- Better input validation on all forms
- .gitignore updated with test and coverage files

### Fixed
- Infinite recursion bug in `distribute_questions()` function
- Session invalidation on server restart
- Missing logout functionality
- Insufficient input validation
- Path traversal vulnerability in file preview
- Missing error handling in database operations

### Security
- Implemented secure session cookies
- Added file upload validation
- Added path traversal protection
- Added comprehensive input validation
- Added logging for security audit trails
- Fixed SECRET_KEY persistence issue

## [1.0.0] - 2025-01-XX

### Added
- Initial release
- Flask-based exam management system
- Teacher dashboard for exam creation
- Student exam interface
- Question allocation system
- File upload for student submissions
- IP-based student authentication
- Exam session management
- Real-time timer for exams
- Bootstrap-based UI
- SQLite database backend
- Support for LTSP netbooting
- Epoptes classroom monitoring integration

[Unreleased]: https://github.com/mfscpayload-690/ExamNetShield/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/mfscpayload-690/ExamNetShield/releases/tag/v1.0.0
