"""
Unit tests for policy-related routes
"""
import pytest
from datetime import date, timedelta
from app import db, SwissAxaPolicy, ExternalPolicy


class TestPoliciesPage:
    """Tests for policies listing page"""
    
    def test_policies_page_loads(self, authenticated_client):
        """Test that policies page loads"""
        response = authenticated_client.get('/policies')
        assert response.status_code == 200
    
    def test_policies_shows_swissaxa_policies(self, authenticated_client, test_policy):
        """Test that SwissAxa policies are displayed"""
        response = authenticated_client.get('/policies')
        assert response.status_code == 200
        assert b'POL-12345' in response.data or b'SwissAxa' in response.data
    
    def test_policies_shows_external_policies(self, authenticated_client, test_external_policy):
        """Test that external policies are displayed"""
        response = authenticated_client.get('/policies')
        assert response.status_code == 200
        assert b'Competitor Insurance' in response.data or b'External' in response.data
    
    def test_policies_expiration_warning(self, test_app, authenticated_client, test_user):
        """Test expiration warning for policies expiring soon"""
        with test_app.app_context():
            # Create a policy expiring in 20 days
            expiring_policy = SwissAxaPolicy(
                user_id=test_user['id'],
                policy_number='POL-EXPIRING',
                policy_type='Test Insurance',
                coverage_amount=10000.00,
                premium=50.00,
                expiration_date=date.today() + timedelta(days=20),
                status='active'
            )
            db.session.add(expiring_policy)
            db.session.commit()
            
            response = authenticated_client.get('/policies')
            assert response.status_code == 200
            # Should show expiration warning
            assert b'Expires' in response.data or b'expiring' in response.data.lower()


class TestExternalPolicyUpload:
    """Tests for external policy upload"""
    
    def test_upload_external_policy_success(self, test_app, authenticated_client, test_user):
        """Test successful external policy upload"""
        with test_app.app_context():
            # Create a temporary file for upload
            import tempfile
            import os
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
            temp_file.write(b'Fake PDF content')
            temp_file.close()
            
            try:
                with open(temp_file.name, 'rb') as f:
                    response = authenticated_client.post('/policies/external/upload', 
                        data={
                            'insurance_company': 'Test Insurance Co',
                            'policy_number': 'TEST-123',
                            'policy_type': 'Auto Insurance',
                            'expiration_date': '2025-12-31',
                            'file': (f, 'test_policy.pdf')
                        },
                        content_type='multipart/form-data',
                        follow_redirects=False
                    )
                
                # Should return success (200 or 302)
                assert response.status_code in [200, 302]
                
                # Verify policy was created
                policy = ExternalPolicy.query.filter_by(policy_number='TEST-123').first()
                assert policy is not None
                assert policy.insurance_company == 'Test Insurance Co'
            finally:
                os.unlink(temp_file.name)
    
    def test_upload_external_policy_no_file(self, authenticated_client):
        """Test upload without file"""
        response = authenticated_client.post('/policies/external/upload', 
            data={
                'insurance_company': 'Test Insurance Co',
                'policy_number': 'TEST-123'
            }
        )
        # Should return error
        assert response.status_code in [400, 200]  # May return error or redirect
    
    def test_upload_external_policy_invalid_data(self, authenticated_client):
        """Test upload with invalid data"""
        response = authenticated_client.post('/policies/external/upload', 
            data={}
        )
        # Should handle error gracefully
        assert response.status_code in [400, 200, 302]


class TestPolicyComparison:
    """Tests for AI-powered policy comparison"""
    
    def test_policy_comparison_api(self, authenticated_client):
        """Test policy comparison API endpoint"""
        response = authenticated_client.post('/api/policy-comparison',
            json={
                'external_policy': {
                    'policy_type': 'Comprehensive Insurance',
                    'premium': 89.99,
                    'coverage': 45000
                }
            },
            content_type='application/json'
        )
        assert response.status_code == 200
        data = response.get_json()
        assert 'similar_products' in data
        assert 'recommendations' in data
        assert len(data['similar_products']) > 0
    
    def test_policy_comparison_requires_auth(self, client):
        """Test that policy comparison requires authentication"""
        response = client.post('/api/policy-comparison',
            json={'external_policy': {}}
        )
        # Should redirect to login or return 401/403
        assert response.status_code in [302, 401, 403]

