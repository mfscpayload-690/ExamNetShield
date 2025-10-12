"""Test configuration and fixtures."""
import pytest
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app as flask_app
from models import db, User, Exam, Student, Question, ExamSession


@pytest.fixture
def app():
    """Create and configure a test app instance."""
    flask_app.config['TESTING'] = True
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    flask_app.config['SECRET_KEY'] = 'test-secret-key'
    flask_app.config['WTF_CSRF_ENABLED'] = False
    
    with flask_app.app_context():
        db.create_all()
        # Create a test user
        test_user = User(username='testuser', password='testpass')
        db.session.add(test_user)
        db.session.commit()
        yield flask_app
        db.drop_all()


@pytest.fixture
def client(app):
    """Create a test client."""
    return app.test_client()


@pytest.fixture
def authenticated_client(client):
    """Create an authenticated test client."""
    client.post('/login', data={
        'username': 'testuser',
        'password': 'testpass'
    })
    return client


@pytest.fixture
def sample_exam(app):
    """Create a sample exam for testing."""
    with app.app_context():
        exam = Exam(
            name='Test Exam',
            duration=2.0,
            reg_number_prefix='TEST',
            reg_number_range='1-5'
        )
        db.session.add(exam)
        db.session.commit()
        
        # Add students
        for i in range(1, 6):
            student = Student(
                registration_number=f'TEST{i:03d}',
                exam_id=exam.id
            )
            db.session.add(student)
        
        # Add questions
        for i in range(1, 4):
            question = Question(
                question_number=i,
                question_text=f'Test question {i}',
                exam_id=exam.id
            )
            db.session.add(question)
        
        db.session.commit()
        return exam
