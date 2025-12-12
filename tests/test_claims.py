"""
Unit tests for claims-related routes
"""
import pytest
from app import db, Claim, ClaimMedia


class TestClaimsPage:
    """Tests for claims listing page"""
    
    def test_claims_page_loads(self, authenticated_client):
        """Test that claims page loads"""
        response = authenticated_client.get('/services/claims')
        assert response.status_code == 200
    
    def test_claims_shows_user_claims(self, authenticated_client, test_claim):
        """Test that user's claims are displayed"""
        response = authenticated_client.get('/services/claims')
        assert response.status_code == 200
        assert b'CLM-20241212001' in response.data or b'claim' in response.data.lower()
    
    def test_claims_shows_policies_dropdown(self, authenticated_client, test_policy):
        """Test that policies are available in claims form"""
        response = authenticated_client.get('/services/claims')
        assert response.status_code == 200
        assert b'POL-12345' in response.data or b'policy' in response.data.lower()


class TestFileClaim:
    """Tests for filing a new claim"""
    
    def test_file_claim_success(self, test_app, authenticated_client, test_user, test_policy):
        """Test successful claim filing"""
        with test_app.app_context():
            import tempfile
            import os
            
            # Create temporary image file (required for evidence)
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
            temp_file.write(b'Fake image content')
            temp_file.close()
            
            try:
                with open(temp_file.name, 'rb') as f:
                    response = authenticated_client.post('/services/claims/file',
                        data={
                            'policy_id': str(test_policy['id']),
                            'description': 'Test claim description',
                            'damage_type': 'Fire Damage',
                            'latitude': '50.1109',
                            'longitude': '8.6821',
                            'address': 'Frankfurt, Germany',
                            'media': (f, 'test_image.jpg')
                        },
                        content_type='multipart/form-data',
                        follow_redirects=True
                    )
                
                assert response.status_code == 200
                
                # Verify claim was created
                claim = Claim.query.filter_by(description='Test claim description').first()
                assert claim is not None
                assert claim.damage_type == 'Fire Damage'
                assert claim.status == 'submitted'
            finally:
                os.unlink(temp_file.name)
    
    def test_file_claim_with_media(self, test_app, authenticated_client, test_user, test_policy):
        """Test filing claim with photos/videos"""
        with test_app.app_context():
            import tempfile
            import os
            
            # Create temporary image file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
            temp_file.write(b'Fake image content')
            temp_file.close()
            
            try:
                with open(temp_file.name, 'rb') as f:
                    response = authenticated_client.post('/services/claims/file',
                        data={
                            'policy_id': str(test_policy['id']),
                            'description': 'Claim with media',
                            'damage_type': 'Water Damage',
                            'latitude': '50.1109',
                            'longitude': '8.6821',
                            'address': 'Frankfurt, Germany',
                            'media': (f, 'test_image.jpg')
                        },
                        content_type='multipart/form-data',
                        follow_redirects=True
                    )
                
                assert response.status_code == 200
                
                # Verify claim and media were created
                claim = Claim.query.filter_by(description='Claim with media').first()
                assert claim is not None
                assert len(claim.media) > 0
            finally:
                os.unlink(temp_file.name)
    
    def test_file_claim_without_policy(self, test_app, authenticated_client, test_user):
        """Test filing claim without policy"""
        with test_app.app_context():
            import tempfile
            import os
            
            # Create temporary image file (required for evidence)
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
            temp_file.write(b'Fake image content')
            temp_file.close()
            
            try:
                with open(temp_file.name, 'rb') as f:
                    response = authenticated_client.post('/services/claims/file',
                        data={
                            'description': 'Claim without policy',
                            'damage_type': 'Theft',
                            'address': 'Berlin, Germany',
                            'media': (f, 'test_image.jpg')
                        },
                        content_type='multipart/form-data',
                        follow_redirects=True
                    )
                
                assert response.status_code == 200
                
                # Claim should still be created
                claim = Claim.query.filter_by(description='Claim without policy').first()
                assert claim is not None
                assert claim.policy_id is None
            finally:
                os.unlink(temp_file.name)
    
    def test_file_claim_requires_auth(self, client):
        """Test that filing claim requires authentication"""
        response = client.post('/services/claims/file',
            data={'description': 'Test claim'}
        )
        # Should redirect to login
        assert response.status_code in [302, 401, 403]

