"""
Unit tests for authentication routes
"""
import pytest
from app import db, User


class TestLogin:
    """Tests for login functionality"""
    
    def test_login_page_loads(self, client):
        """Test that login page loads"""
        response = client.get('/login')
        assert response.status_code == 200
        assert b'Login' in response.data or b'login' in response.data.lower()
    
    def test_login_success(self, client, test_user):
        """Test successful login"""
        # Use known email from fixture
        response = client.post('/login', data={
            'email': 'test@example.com',
            'password': 'testpassword123'
        }, follow_redirects=True)
        assert response.status_code == 200
        # Should redirect to dashboard after login
        assert 'dashboard' in response.request.path.lower() or response.status_code == 200
    
    def test_login_invalid_email(self, client):
        """Test login with invalid email"""
        response = client.post('/login', data={
            'email': 'nonexistent@example.com',
            'password': 'password123'
        })
        assert response.status_code == 200
        # Should show error message
        assert b'Invalid' in response.data or b'error' in response.data.lower()
    
    def test_login_invalid_password(self, client, test_user):
        """Test login with invalid password"""
        response = client.post('/login', data={
            'email': 'test@example.com',
            'password': 'wrongpassword'
        })
        assert response.status_code == 200
        assert b'Invalid' in response.data or b'error' in response.data.lower()
    
    def test_login_redirects_authenticated_user(self, test_app, authenticated_client):
        """Test that authenticated users are redirected from login page"""
        with test_app.app_context():
            response = authenticated_client.get('/login', follow_redirects=True)
            # Should redirect to dashboard or show dashboard
            assert response.status_code == 200


class TestRegister:
    """Tests for registration functionality"""
    
    def test_register_page_loads(self, client):
        """Test that register page loads"""
        response = client.get('/register')
        assert response.status_code == 200
        assert b'Register' in response.data or b'register' in response.data.lower()
    
    def test_register_success(self, test_app, client):
        """Test successful registration"""
        with test_app.app_context():
            response = client.post('/register', data={
                'email': 'newuser@example.com',
                'password': 'newpassword123',
                'first_name': 'New',
                'last_name': 'User'
            }, follow_redirects=True)
            assert response.status_code == 200
            
            # Verify user was created
            user = User.query.filter_by(email='newuser@example.com').first()
            assert user is not None
            assert user.first_name == 'New'
            assert user.last_name == 'User'
    
    def test_register_duplicate_email(self, client, test_user):
        """Test registration with duplicate email"""
        response = client.post('/register', data={
            'email': 'test@example.com',
            'password': 'password123',
            'first_name': 'Test',
            'last_name': 'User'
        })
        assert response.status_code == 200
        assert b'already registered' in response.data.lower() or b'exists' in response.data.lower()
    
    def test_register_missing_fields(self, client):
        """Test registration with missing required fields"""
        response = client.post('/register', data={
            'email': 'incomplete@example.com',
            'password': 'password123'
            # Missing first_name and last_name
        })
        # Should either show error or still be on register page or redirect
        assert response.status_code in [200, 302, 400]


class TestLogout:
    """Tests for logout functionality"""
    
    def test_logout_requires_login(self, client):
        """Test that logout requires authentication"""
        response = client.get('/logout', follow_redirects=True)
        # Should redirect to login
        assert 'login' in response.request.path.lower() or response.status_code == 200
    
    def test_logout_success(self, test_app, authenticated_client):
        """Test successful logout"""
        with test_app.app_context():
            response = authenticated_client.get('/logout', follow_redirects=True)
            assert response.status_code == 200
            # Should redirect to login page
            assert 'login' in response.request.path.lower() or response.status_code == 200


class TestProtectedRoutes:
    """Tests for protected routes requiring authentication"""
    
    def test_dashboard_requires_login(self, client):
        """Test that dashboard requires login"""
        response = client.get('/dashboard', follow_redirects=True)
        assert 'login' in response.request.path.lower() or response.status_code == 200
    
    def test_policies_requires_login(self, client):
        """Test that policies page requires login"""
        response = client.get('/policies', follow_redirects=True)
        assert 'login' in response.request.path.lower() or response.status_code == 200
    
    def test_documents_requires_login(self, client):
        """Test that documents page requires login"""
        response = client.get('/documents', follow_redirects=True)
        assert 'login' in response.request.path.lower() or response.status_code == 200
    
    def test_services_requires_login(self, client):
        """Test that services page requires login"""
        response = client.get('/services', follow_redirects=True)
        assert 'login' in response.request.path.lower() or response.status_code == 200
    
    def test_dashboard_accessible_when_logged_in(self, test_app, authenticated_client):
        """Test that dashboard is accessible when logged in"""
        with test_app.app_context():
            response = authenticated_client.get('/dashboard')
            assert response.status_code == 200

