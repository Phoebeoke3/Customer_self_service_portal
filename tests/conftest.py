"""
Pytest configuration and fixtures for SwissAxa Portal tests
"""
import pytest
import os
import tempfile
import shutil
from datetime import datetime, date, timedelta
from flask import Flask

# Import app components
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db, User, Agent, SwissAxaPolicy, ExternalPolicy, Document, Claim, ClaimMedia, PolicyChangeRequest, Appointment, BankAccount


@pytest.fixture(scope='function')
def test_app():
    """Create a test Flask application with test database"""
    # Create temporary database
    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SECRET_KEY'] = 'test-secret-key'
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['UPLOAD_FOLDER'] = tempfile.mkdtemp()
    
    # Create upload directories
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'documents'), exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'policies'), exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'claims'), exist_ok=True)
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()
    
    # Cleanup
    os.close(db_fd)
    os.unlink(db_path)
    shutil.rmtree(app.config['UPLOAD_FOLDER'])


@pytest.fixture(scope='function')
def client(test_app):
    """Create a test client"""
    return test_app.test_client()


@pytest.fixture(scope='function')
def authenticated_client(test_app, test_user):
    """Create an authenticated test client"""
    client = test_app.test_client()
    # Login the user - need to access email within app context
    with test_app.app_context():
        # Merge user into current session or get email directly
        user_email = 'test@example.com'  # Use known email from fixture
        response = client.post('/login', data={
            'email': user_email,
            'password': 'testpassword123'
        }, follow_redirects=False)
    return client


@pytest.fixture(scope='function')
def test_user(test_app):
    """Create a test user"""
    with test_app.app_context():
        user = User(
            email='test@example.com',
            first_name='Test',
            last_name='User',
            phone='+49 123 456789',
            address='Test Street 123, Berlin',
            correspondence_address='Test Street 123, Berlin'
        )
        user.set_password('testpassword123')
        db.session.add(user)
        db.session.commit()
        user_id = user.id
        # Expunge to detach, but store ID for re-querying
        db.session.expunge(user)
        return {'user': user, 'id': user_id, 'email': 'test@example.com'}


@pytest.fixture(scope='function')
def test_agent(test_app):
    """Create a test agent"""
    with test_app.app_context():
        agent = Agent(
            name='Test Agent',
            email='agent@swissaxa.de',
            phone='+49 221 123456'
        )
        db.session.add(agent)
        db.session.commit()
        agent_id = agent.id
        db.session.expunge(agent)
        return {'agent': agent, 'id': agent_id, 'email': 'agent@swissaxa.de'}


@pytest.fixture(scope='function')
def test_policy(test_app, test_user):
    """Create a test SwissAxa policy"""
    with test_app.app_context():
        policy = SwissAxaPolicy(
            user_id=test_user['id'],
            policy_number='POL-12345',
            policy_type='Comprehensive Insurance',
            coverage_amount=50000.00,
            premium=99.99,
            expiration_date=date.today() + timedelta(days=365),
            status='active'
        )
        db.session.add(policy)
        db.session.commit()
        policy_id = policy.id
        db.session.expunge(policy)
        return {'policy': policy, 'id': policy_id, 'policy_number': 'POL-12345'}


@pytest.fixture(scope='function')
def test_external_policy(test_app, test_user):
    """Create a test external policy"""
    with test_app.app_context():
        external_policy = ExternalPolicy(
            user_id=test_user['id'],
            insurance_company='Competitor Insurance',
            policy_number='EXT-67890',
            policy_type='General Insurance',
            expiration_date=date.today() + timedelta(days=180),
            file_path='test_policy.pdf'
        )
        db.session.add(external_policy)
        db.session.commit()
        policy_id = external_policy.id
        db.session.expunge(external_policy)
        return {'policy': external_policy, 'id': policy_id, 'insurance_company': 'Competitor Insurance'}


@pytest.fixture(scope='function')
def test_claim(test_app, test_user, test_policy):
    """Create a test claim"""
    with test_app.app_context():
        claim = Claim(
            user_id=test_user['id'],
            policy_id=test_policy['id'],
            claim_number='CLM-20241212001',
            description='Test claim description',
            damage_type='Water Damage',
            latitude=50.1109,
            longitude=8.6821,
            address='Frankfurt, Germany',
            status='submitted'
        )
        db.session.add(claim)
        db.session.commit()
        claim_id = claim.id
        db.session.expunge(claim)
        return {'claim': claim, 'id': claim_id, 'claim_number': 'CLM-20241212001'}


@pytest.fixture(scope='function')
def test_document(test_app, test_user):
    """Create a test document"""
    with test_app.app_context():
        document = Document(
            user_id=test_user['id'],
            filename='test_document.pdf',
            file_path='uploads/documents/test_document.pdf',
            document_type='policy'
        )
        db.session.add(document)
        db.session.commit()
        doc_id = document.id
        db.session.expunge(document)
        return {'document': document, 'id': doc_id, 'filename': 'test_document.pdf'}


@pytest.fixture(scope='function')
def test_bank_account(test_app, test_user):
    """Create a test bank account"""
    with test_app.app_context():
        bank_account = BankAccount(
            user_id=test_user['id'],
            bank_name='Sparkasse',
            account_number='DE89370400440532013000',
            is_connected=True
        )
        db.session.add(bank_account)
        db.session.commit()
        account_id = bank_account.id
        db.session.expunge(bank_account)
        return {'account': bank_account, 'id': account_id, 'bank_name': 'Sparkasse'}


@pytest.fixture(scope='function')
def test_appointment(test_app, test_user, test_agent):
    """Create a test appointment"""
    with test_app.app_context():
        appointment = Appointment(
            user_id=test_user['id'],
            agent_id=test_agent['id'],
            appointment_type='agent',
            date_time=datetime.now() + timedelta(days=7),
            purpose='Policy consultation',
            status='scheduled'
        )
        db.session.add(appointment)
        db.session.commit()
        appointment_id = appointment.id
        db.session.expunge(appointment)
        return {'appointment': appointment, 'id': appointment_id}

