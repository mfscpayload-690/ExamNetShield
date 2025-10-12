"""Test authentication and basic routes."""
import pytest


class TestAuthentication:
    """Test authentication functionality."""
    
    def test_login_page_loads(self, client):
        """Test that login page loads successfully."""
        response = client.get('/login')
        assert response.status_code == 200
        
    def test_successful_login(self, client):
        """Test successful login."""
        response = client.post('/login', data={
            'username': 'testuser',
            'password': 'testpass'
        }, follow_redirects=True)
        assert response.status_code == 200
        assert b'Login successful' in response.data or b'Exam' in response.data
        
    def test_failed_login_wrong_password(self, client):
        """Test login with wrong password."""
        response = client.post('/login', data={
            'username': 'testuser',
            'password': 'wrongpass'
        }, follow_redirects=True)
        assert b'Invalid credentials' in response.data
        
    def test_failed_login_wrong_username(self, client):
        """Test login with non-existent username."""
        response = client.post('/login', data={
            'username': 'nonexistent',
            'password': 'testpass'
        }, follow_redirects=True)
        assert b'Invalid credentials' in response.data
        
    def test_logout(self, authenticated_client):
        """Test logout functionality."""
        response = authenticated_client.get('/logout', follow_redirects=True)
        assert response.status_code == 200
        assert b'logged out' in response.data
        
    def test_protected_route_requires_login(self, client):
        """Test that protected routes require login."""
        response = client.get('/create_exam', follow_redirects=True)
        assert b'login' in response.data.lower()


class TestDistributeQuestions:
    """Test question distribution algorithm."""
    
    def test_distribute_questions_basic(self):
        """Test basic question distribution."""
        from app import distribute_questions
        
        questions = ['Q1', 'Q2', 'Q3']
        result = distribute_questions(6, questions)
        
        assert len(result) == 6
        assert all(q in questions for q in result)
        
    def test_distribute_questions_adjacent_different(self):
        """Test that adjacent students don't get same question."""
        from app import distribute_questions
        
        questions = ['Q1', 'Q2', 'Q3']
        result = distribute_questions(10, questions)
        
        for i in range(1, len(result)):
            # Adjacent students should have different questions (when possible)
            if len(questions) > 1:
                assert result[i] != result[i-1] or len(questions) == 1
                
    def test_distribute_questions_single_question(self):
        """Test distribution with only one question."""
        from app import distribute_questions
        
        questions = ['Q1']
        result = distribute_questions(5, questions)
        
        assert len(result) == 5
        assert all(q == 'Q1' for q in result)
        
    def test_distribute_questions_empty(self):
        """Test distribution with no students."""
        from app import distribute_questions
        
        questions = ['Q1', 'Q2']
        result = distribute_questions(0, questions)
        
        assert len(result) == 0
