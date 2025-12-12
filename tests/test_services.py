"""
Unit tests for services-related routes
"""
import pytest
from datetime import datetime, timedelta
from app import db, PolicyChangeRequest, Appointment, Agent


class TestServicesPage:
    """Tests for services page"""
    
    def test_services_page_loads(self, authenticated_client):
        """Test that services page loads"""
        response = authenticated_client.get('/services')
        assert response.status_code == 200


class TestPolicyManagement:
    """Tests for policy management"""
    
    def test_policy_management_page_loads(self, authenticated_client):
        """Test that policy management page loads"""
        response = authenticated_client.get('/services/policy-management')
        assert response.status_code == 200
    
    def test_policy_management_shows_policies(self, authenticated_client, test_policy):
        """Test that policies are displayed"""
        response = authenticated_client.get('/services/policy-management')
        assert response.status_code == 200
        assert b'POL-12345' in response.data or b'policy' in response.data.lower()
    
    def test_submit_policy_change_request(self, test_app, authenticated_client, test_user, test_policy):
        """Test submitting a policy change request"""
        with test_app.app_context():
            response = authenticated_client.post('/services/policy-management/request',
                data={
                    'policy_id': str(test_policy['id']),
                    'request_type': 'upgrade',
                    'description': 'I want to upgrade my policy'
                },
                follow_redirects=True
            )
            assert response.status_code == 200
            
            # Verify request was created
            request = PolicyChangeRequest.query.filter_by(
                user_id=test_user['id'],
                request_type='upgrade'
            ).first()
            assert request is not None
            assert request.description == 'I want to upgrade my policy'
            assert request.status == 'pending'


class TestContact:
    """Tests for contact functionality"""
    
    def test_contact_page_loads(self, authenticated_client):
        """Test that contact page loads"""
        response = authenticated_client.get('/services/contact')
        assert response.status_code == 200
    
    def test_contact_shows_agents(self, authenticated_client, test_agent):
        """Test that agents are displayed"""
        response = authenticated_client.get('/services/contact')
        assert response.status_code == 200
        assert b'agent@swissaxa.de' in response.data or b'agent' in response.data.lower()
    
    def test_send_email_to_service_desk(self, authenticated_client):
        """Test sending email to service desk"""
        response = authenticated_client.post('/services/contact',
            data={
                'recipient_type': 'service_desk',
                'recipient_email': 'service@swissaxa.de',
                'subject': 'Test Subject',
                'message': 'Test message'
            },
            follow_redirects=True
        )
        assert response.status_code == 200
        # Should show success message
        assert b'sent' in response.data.lower() or b'success' in response.data.lower()
    
    def test_send_email_to_agent(self, authenticated_client, test_agent):
        """Test sending email to agent"""
        response = authenticated_client.post('/services/contact',
            data={
                'recipient_type': 'agent',
                'recipient_email': test_agent['email'],
                'subject': 'Test Subject',
                'message': 'Test message'
            },
            follow_redirects=True
        )
        assert response.status_code == 200
        assert b'sent' in response.data.lower() or b'success' in response.data.lower()


class TestScheduling:
    """Tests for appointment scheduling"""
    
    def test_scheduling_page_loads(self, authenticated_client):
        """Test that scheduling page loads"""
        response = authenticated_client.get('/services/scheduling')
        assert response.status_code == 200
    
    def test_scheduling_shows_agents(self, authenticated_client, test_agent):
        """Test that agents are available for scheduling"""
        response = authenticated_client.get('/services/scheduling')
        assert response.status_code == 200
        assert b'agent' in response.data.lower()
    
    def test_book_appointment_with_agent(self, test_app, authenticated_client, test_user, test_agent):
        """Test booking appointment with agent"""
        with test_app.app_context():
            appointment_time = datetime.now() + timedelta(days=7)
            response = authenticated_client.post('/services/scheduling',
                data={
                    'agent_id': str(test_agent['id']),
                    'appointment_type': 'agent',
                    'date_time': appointment_time.strftime('%Y-%m-%dT%H:%M'),
                    'purpose': 'Policy consultation'
                },
                follow_redirects=True
            )
            assert response.status_code == 200
            
            # Verify appointment was created
            appointment = Appointment.query.filter_by(
                user_id=test_user['id'],
                agent_id=test_agent['id']
            ).first()
            assert appointment is not None
            assert appointment.appointment_type == 'agent'
            assert appointment.status == 'scheduled'
    
    def test_book_appointment_with_service_desk(self, test_app, authenticated_client, test_user):
        """Test booking appointment with service desk"""
        with test_app.app_context():
            appointment_time = datetime.now() + timedelta(days=5)
            response = authenticated_client.post('/services/scheduling',
                data={
                    'appointment_type': 'service_desk',
                    'date_time': appointment_time.strftime('%Y-%m-%dT%H:%M'),
                    'purpose': 'General inquiry'
                },
                follow_redirects=True
            )
            assert response.status_code == 200
            
            # Verify appointment was created
            appointment = Appointment.query.filter_by(
                user_id=test_user['id'],
                appointment_type='service_desk'
            ).first()
            assert appointment is not None
            assert appointment.agent_id is None

