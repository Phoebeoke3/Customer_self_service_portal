"""
Unit tests for user information routes
"""
import pytest
from app import db, User


class TestInformationPage:
    """Tests for information page"""
    
    def test_information_page_loads(self, authenticated_client, test_user):
        """Test that information page loads"""
        response = authenticated_client.get('/information')
        assert response.status_code == 200
        assert b'test@example.com' in response.data or b'Test' in response.data
    
    def test_information_shows_user_data(self, authenticated_client, test_user):
        """Test that user data is displayed"""
        response = authenticated_client.get('/information')
        assert response.status_code == 200
        assert b'Test User' in response.data or b'Test' in response.data


class TestUpdateInformation:
    """Tests for updating user information"""
    
    def test_update_information_success(self, test_app, authenticated_client, test_user):
        """Test successful information update"""
        with test_app.app_context():
            response = authenticated_client.post('/information/update',
                data={
                    'first_name': 'Updated',
                    'last_name': 'Name',
                    'phone': '+49 999 888777',
                    'address': 'New Address 456, Munich',
                    'correspondence_address': 'New Address 456, Munich',
                    'bank_account': 'DE12345678901234567890'
                },
                follow_redirects=True
            )
            assert response.status_code == 200
            
            # Verify information was updated
            user = User.query.get(test_user['id'])
            assert user.first_name == 'Updated'
            assert user.last_name == 'Name'
            assert user.phone == '+49 999 888777'
            assert user.address == 'New Address 456, Munich'
    
    def test_update_information_partial(self, test_app, authenticated_client, test_user):
        """Test partial information update"""
        with test_app.app_context():
            user = User.query.get(test_user['id'])
            original_phone = user.phone
            response = authenticated_client.post('/information/update',
                data={
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'phone': '+49 111 222333',
                    'address': user.address,
                    'correspondence_address': user.correspondence_address
                },
                follow_redirects=True
            )
            assert response.status_code == 200
            
            # Verify only phone was updated
            db.session.refresh(user)
            assert user.phone == '+49 111 222333'
            assert user.first_name == 'Test'  # Should remain unchanged
    
    def test_update_information_requires_auth(self, client):
        """Test that updating information requires authentication"""
        response = client.post('/information/update',
            data={'first_name': 'Test'}
        )
        # Should redirect to login
        assert response.status_code in [302, 401, 403]

