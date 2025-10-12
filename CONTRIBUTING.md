# Contributing to ExamNetShield

Thank you for your interest in contributing to ExamNetShield! This document provides guidelines for contributing to the project.

## Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git

### Setup Development Environment

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/ExamNetShield.git
   cd ExamNetShield
   ```

3. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # If available
   ```

5. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

6. Edit `.env` and set your configuration values

7. Create the initial database:
   ```bash
   python create_user.py
   ```

## Development Workflow

### Before Making Changes

1. Create a new branch for your feature/fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make sure the application runs:
   ```bash
   python app.py
   ```

### Making Changes

1. Write clean, readable code following PEP 8 style guide
2. Add docstrings to functions and classes
3. Add comments for complex logic
4. Update documentation if needed
5. Add tests for new features

### Testing

Run tests before committing:
```bash
python -m pytest tests/
```

Check code style:
```bash
flake8 app.py models.py utils.py
```

### Committing Changes

1. Stage your changes:
   ```bash
   git add .
   ```

2. Commit with a descriptive message:
   ```bash
   git commit -m "Add feature: description of your changes"
   ```

3. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

4. Create a Pull Request from your fork to the main repository

## Pull Request Guidelines

### Before Submitting

- [ ] Code follows PEP 8 style guide
- [ ] All tests pass
- [ ] New features have tests
- [ ] Documentation is updated
- [ ] Commit messages are clear and descriptive

### PR Description Should Include

1. **What**: Brief description of changes
2. **Why**: Reason for the changes
3. **How**: How the changes work
4. **Testing**: How you tested the changes
5. **Screenshots**: For UI changes

## Code Style

### Python Code Style

- Follow PEP 8
- Use 4 spaces for indentation
- Maximum line length: 100 characters
- Use meaningful variable and function names
- Add docstrings to all functions and classes

Example:
```python
def calculate_grade(score, total):
    """
    Calculate the percentage grade.
    
    Args:
        score (int): Points earned
        total (int): Total possible points
        
    Returns:
        float: Percentage grade
    """
    if total == 0:
        return 0.0
    return (score / total) * 100
```

### Commit Message Format

```
<type>: <subject>

<body>

<footer>
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, missing semicolons, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Example:
```
feat: Add logout functionality for teachers

- Add logout route in app.py
- Update navigation bar with logout button
- Clear session on logout
- Add logging for logout events
```

## Reporting Bugs

### Before Reporting

1. Check if the bug has already been reported
2. Try to reproduce the bug on the latest version
3. Collect relevant information (error messages, logs, screenshots)

### Bug Report Should Include

- **Description**: Clear description of the bug
- **Steps to Reproduce**: Step-by-step instructions
- **Expected Behavior**: What should happen
- **Actual Behavior**: What actually happens
- **Environment**: OS, Python version, browser
- **Screenshots**: If applicable
- **Logs**: Relevant error messages or logs

## Suggesting Enhancements

### Enhancement Suggestions Should Include

- **Use Case**: Why this enhancement would be useful
- **Description**: Clear description of the enhancement
- **Examples**: Examples of how it would work
- **Alternatives**: Alternative solutions considered

## Security

If you discover a security vulnerability, please email the maintainer directly instead of opening a public issue. See the README for contact information.

## Questions?

Feel free to open an issue with the label "question" if you have any questions about contributing.

## License

By contributing to ExamNetShield, you agree that your contributions will be licensed under the MIT License.

## Thank You!

Your contributions are greatly appreciated! 🙏
