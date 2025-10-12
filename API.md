# API Documentation

## Overview

ExamNetShield provides a Flask-based web API for managing exams. This document describes the available endpoints and their usage.

## Authentication

Most endpoints require session-based authentication. Login as a teacher to access administrative endpoints.

### Login

**Endpoint:** `POST /login`

**Parameters:**
- `username` (string, required): Teacher username
- `password` (string, required): Teacher password

**Response:** Redirects to `/create_exam` on success

**Example:**
```bash
curl -X POST http://localhost:5000/login \
  -d "username=admin&password=password"
```

### Logout

**Endpoint:** `GET /logout`

**Authentication:** Required

**Response:** Redirects to `/login`

## Exam Management

### Create Exam

**Endpoint:** `POST /create_exam`

**Authentication:** Required

**Parameters:**
- `name` (string, required): Exam name
- `duration` (float, required): Duration in hours (0-24)
- `reg_prefix` (string, required): Registration number prefix
- `reg_range` (string, required): Range in format "start-end" (e.g., "1-50")

**Response:** Redirects to `/add_questions/<exam_id>` on success

**Example:**
```bash
curl -X POST http://localhost:5000/create_exam \
  -H "Cookie: session=..." \
  -d "name=Midterm Exam&duration=2.0&reg_prefix=CS&reg_range=1-30"
```

### View Exam Details

**Endpoint:** `GET /exam/<exam_id>`

**Authentication:** Required

**Response:** HTML page with exam details

### Add Question

**Endpoint:** `POST /add_questions/<exam_id>`

**Authentication:** Required

**Parameters:**
- `question_number` (integer, required): Question number
- `question_text` (string, required): Question text (max 5000 chars)

**Response:** Redirects back to add questions page

**Example:**
```bash
curl -X POST http://localhost:5000/add_questions/1 \
  -H "Cookie: session=..." \
  -d "question_number=1&question_text=What is polymorphism?"
```

### Start Exam

**Endpoint:** `POST /start_exam`

**Authentication:** Required

**Parameters:**
- `exam_id` (integer, required): ID of the exam to start

**Response:** Redirects to exam details page

**Notes:**
- Assigns questions to students
- Marks exam as started
- Students can then login and take the exam

### Stop Exam

**Endpoint:** `POST /stop_exam`

**Authentication:** Required

**Parameters:**
- `exam_id` (integer, required): ID of the exam to stop

**Response:** Redirects to exam details page

**Notes:**
- Marks exam as ended
- Prevents further student submissions

## Student Operations

### Student Registration

**Endpoint:** `POST /register`

**Authentication:** Not required

**Parameters:**
- `reg_number` (string, required): Student registration number
- `exam_id` (integer, required): ID of the exam

**Response:** Redirects to student exam page

**Notes:**
- Validates registration number
- Binds student to IP address
- Prevents login from different IP

### Student Exam Page

**Endpoint:** `GET /student_exam/<student_id>`

**Authentication:** Not required (but student must be registered)

**Response:** HTML page with assigned question

### Submit Answer

**Endpoint:** `POST /student_exam/<student_id>`

**Parameters:**
- `answer_file` (file, required): Student's answer file

**Response:** Redirects to registration page

**Allowed file types:**
- .txt, .pdf, .png, .jpg, .jpeg, .gif
- .py, .java, .c, .cpp, .js, .html, .css
- .zip, .docx

**Example:**
```bash
curl -X POST http://localhost:5000/student_exam/1 \
  -F "answer_file=@answer.pdf"
```

### Start Exam Session

**Endpoint:** `POST /exam/start`

**Parameters:**
- `student_id` (integer, required): Student ID
- `exam_id` (integer, required): Exam ID

**Response:** JSON with remaining time

**Example:**
```bash
curl -X POST http://localhost:5000/exam/start \
  -H "Content-Type: application/json" \
  -d '{"student_id": 1, "exam_id": 1}'
```

**Response:**
```json
{
  "remaining_time": 7200
}
```

## File Management

### Preview Answer

**Endpoint:** `GET /preview_answer/<path:file_path>`

**Authentication:** Required

**Query Parameters:**
- `download` (optional): Set to "true" to download instead of preview

**Response:** File content or download

**Example:**
```bash
# Preview
curl http://localhost:5000/preview_answer/1/CS001/answer.txt

# Download
curl http://localhost:5000/preview_answer/1/CS001/answer.txt?download=true
```

## Data Models

### User
```python
{
  "id": integer,
  "username": string,
  "password": string (hashed)
}
```

### Exam
```python
{
  "id": integer,
  "name": string,
  "duration": float,
  "reg_number_prefix": string,
  "reg_number_range": string,
  "is_started": boolean,
  "is_ended": boolean
}
```

### Student
```python
{
  "id": integer,
  "registration_number": string,
  "exam_id": integer,
  "ip_address": string,
  "allocated_questions": string,
  "submitted_file": string
}
```

### Question
```python
{
  "id": integer,
  "question_number": integer,
  "question_text": string,
  "exam_id": integer
}
```

### ExamSession
```python
{
  "id": integer,
  "student_id": integer,
  "exam_id": integer,
  "start_time": datetime,
  "duration": integer,
  "is_closed": boolean
}
```

## Error Responses

### 400 Bad Request
```json
{
  "error": "Invalid request parameters"
}
```

### 401 Unauthorized
Redirects to login page

### 404 Not Found
```json
{
  "error": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error"
}
```

## Rate Limiting

Currently, no rate limiting is implemented. Consider adding rate limiting for production use.

## Best Practices

1. **Always use HTTPS in production**
2. **Validate all inputs on the client side** before sending to server
3. **Handle errors gracefully** in your client application
4. **Store session cookies securely**
5. **Implement CSRF protection** when integrating with other applications

## Future API Enhancements

- RESTful API endpoints
- JSON responses for all operations
- API authentication tokens
- Batch operations
- Webhooks for exam events
- Real-time updates via WebSockets
