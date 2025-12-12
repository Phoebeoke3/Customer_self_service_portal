"""
Unit tests for database models
"""
import pytest
from datetime import date, datetime, timedelta
from app import db, User, Agent, SwissAxaPolicy, ExternalPolicy, Document, Claim, ClaimMedia, PolicyChangeRequest, Appointment, BankAccount


class TestUserModel:
    """Tests for User model"""
    
    def test_user_creation(self, test_app, test_user):
        """Test creating a user"""
        with test_app.app_context():
            user = db.session.merge(test_user['user'])
            assert user.id is not None
            assert user.email == 'test@example.com'
            assert user.first_name == 'Test'
            assert user.last_name == 'User'
    
    def test_user_password_hashing(self, test_app):
        """Test password hashing"""
        with test_app.app_context():
            user = User(email='test2@example.com', first_name='Test', last_name='User')
            user.set_password('mypassword')
            assert user.password_hash != 'mypassword'
            assert user.check_password('mypassword') is True
            assert user.check_password('wrongpassword') is False
    
    def test_user_unique_email(self, test_app, test_user):
        """Test that email must be unique"""
        with test_app.app_context():
            duplicate_user = User(email='test@example.com', first_name='Another', last_name='User')
            db.session.add(duplicate_user)
            with pytest.raises(Exception):  # SQLAlchemy raises IntegrityError
                db.session.commit()


class TestAgentModel:
    """Tests for Agent model"""
    
    def test_agent_creation(self, test_app, test_agent):
        """Test creating an agent"""
        with test_app.app_context():
            agent = db.session.merge(test_agent['agent'])
            assert agent.id is not None
            assert agent.name == 'Test Agent'
            assert agent.email == 'agent@swissaxa.de'
            assert agent.phone == '+49 221 123456'


class TestSwissAxaPolicyModel:
    """Tests for SwissAxaPolicy model"""
    
    def test_policy_creation(self, test_app, test_policy):
        """Test creating a policy"""
        with test_app.app_context():
            policy = db.session.merge(test_policy['policy'])
            assert policy.id is not None
            assert policy.policy_number == 'POL-12345'
            assert policy.policy_type == 'Comprehensive Insurance'
            assert policy.coverage_amount == 50000.00
            assert policy.premium == 99.99
            assert policy.status == 'active'
            assert policy.user_id is not None
    
    def test_policy_user_relationship(self, test_app, test_user, test_policy):
        """Test policy-user relationship"""
        with test_app.app_context():
            policy = db.session.merge(test_policy['policy'])
            user = db.session.merge(test_user['user'])
            assert policy.user.id == user.id
            assert len(user.swissaxa_policies) > 0
            assert user.swissaxa_policies[0].policy_number == 'POL-12345'


class TestExternalPolicyModel:
    """Tests for ExternalPolicy model"""
    
    def test_external_policy_creation(self, test_app, test_external_policy):
        """Test creating an external policy"""
        with test_app.app_context():
            policy = db.session.merge(test_external_policy['policy'])
            assert policy.id is not None
            assert policy.insurance_company == 'Competitor Insurance'
            assert policy.policy_number == 'EXT-67890'
            assert policy.user_id is not None


class TestClaimModel:
    """Tests for Claim model"""
    
    def test_claim_creation(self, test_app, test_claim):
        """Test creating a claim"""
        with test_app.app_context():
            claim = db.session.merge(test_claim['claim'])
            assert claim.id is not None
            assert claim.claim_number == 'CLM-20241212001'
            assert claim.description == 'Test claim description'
            assert claim.damage_type == 'Water Damage'
            assert claim.status == 'submitted'
            assert claim.latitude == 50.1109
            assert claim.longitude == 8.6821
    
    def test_claim_user_relationship(self, test_app, test_user, test_claim):
        """Test claim-user relationship"""
        with test_app.app_context():
            claim = db.session.merge(test_claim['claim'])
            user = db.session.merge(test_user['user'])
            assert claim.user.id == user.id
            assert len(user.claims) > 0


class TestDocumentModel:
    """Tests for Document model"""
    
    def test_document_creation(self, test_app, test_document):
        """Test creating a document"""
        with test_app.app_context():
            document = db.session.merge(test_document['document'])
            assert document.id is not None
            assert document.filename == 'test_document.pdf'
            assert document.document_type == 'policy'
            assert document.user_id is not None


class TestBankAccountModel:
    """Tests for BankAccount model"""
    
    def test_bank_account_creation(self, test_app, test_bank_account):
        """Test creating a bank account"""
        with test_app.app_context():
            account = db.session.merge(test_bank_account['account'])
            assert account.id is not None
            assert account.bank_name == 'Sparkasse'
            assert account.account_number == 'DE89370400440532013000'
            assert account.is_connected is True


class TestAppointmentModel:
    """Tests for Appointment model"""
    
    def test_appointment_creation(self, test_app, test_appointment):
        """Test creating an appointment"""
        with test_app.app_context():
            appointment = db.session.merge(test_appointment['appointment'])
            assert appointment.id is not None
            assert appointment.appointment_type == 'agent'
            assert appointment.purpose == 'Policy consultation'
            assert appointment.status == 'scheduled'
            assert appointment.user_id is not None
            assert appointment.agent_id is not None

