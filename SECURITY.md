# Security Policy

## Supported Versions

Currently, we support security updates for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take security vulnerabilities seriously. If you discover a security issue, please follow these steps:

### 1. Do Not Publicly Disclose

Please do not open a public GitHub issue for security vulnerabilities. This helps protect users until a fix is available.

### 2. Contact Us Privately

Email the maintainer directly at the contact information provided in the README.md file.

Include the following information:
- Description of the vulnerability
- Steps to reproduce the issue
- Potential impact
- Any suggested fixes (if available)

### 3. Response Timeline

- **Initial Response**: Within 48 hours
- **Status Update**: Within 7 days
- **Fix Timeline**: Depends on severity
  - Critical: Within 7 days
  - High: Within 14 days
  - Medium: Within 30 days
  - Low: Next regular release

## Security Best Practices for Users

### 1. Environment Configuration

- Always use strong, unique `SECRET_KEY` in production
- Set `DEBUG=False` in production
- Use HTTPS in production environments
- Enable `SESSION_COOKIE_SECURE=True` when using HTTPS

### 2. Database Security

- Use proper database permissions
- Regularly backup your database
- Consider using PostgreSQL or MySQL instead of SQLite for production

### 3. File Upload Security

- Configure maximum file size limits
- Regularly review uploaded files
- Consider virus scanning for uploaded files
- Store uploads outside the web root if possible

### 4. Access Control

- Change default admin credentials immediately
- Use strong passwords
- Implement regular password rotation
- Limit teacher account access

### 5. Network Security

- Use firewalls to restrict access
- Implement rate limiting
- Monitor for unusual activity
- Keep the system updated

### 6. Monitoring and Logging

- Regularly review application logs
- Set up alerts for suspicious activity
- Monitor failed login attempts
- Track file upload patterns

## Known Security Considerations

### File Upload

The application accepts file uploads from students. By default, the following file types are allowed:
- Text files (.txt)
- PDF files (.pdf)
- Image files (.png, .jpg, .jpeg, .gif)
- Code files (.py, .java, .c, .cpp, .js, .html, .css)
- Archive files (.zip)
- Document files (.docx)

Consider implementing:
- File size limits (configured via `MAX_CONTENT_LENGTH`)
- Virus scanning for uploaded files
- Regular cleanup of old uploads

### Session Management

- Sessions expire after 1 hour by default (configurable)
- Sessions are cleared on logout
- Consider implementing CSRF protection for forms

### Database

- SQLite is used by default (suitable for development/small deployments)
- For production, consider PostgreSQL or MySQL
- Implement regular backups

### Password Storage

- Passwords are hashed using Werkzeug's `generate_password_hash`
- Uses PBKDF2 with SHA256 by default
- Consider implementing password complexity requirements

## Security Updates

We will:
- Promptly address reported security issues
- Release security patches as needed
- Update this policy as the project evolves
- Notify users of critical security updates

## Third-Party Dependencies

We monitor our dependencies for known vulnerabilities:
- Regular dependency updates
- Automated vulnerability scanning via GitHub Actions
- Use of tools like `safety` and `bandit`

To check dependencies yourself:
```bash
pip install safety
safety check -r requirements.txt
```

## Compliance

This application is designed for educational use in controlled environments. Organizations should:
- Review local data protection regulations
- Implement appropriate access controls
- Ensure proper data handling procedures
- Maintain audit logs

## Attribution

If you responsibly disclose a security vulnerability and would like to be credited, please let us know how you would like to be acknowledged.
