"""
Unit tests for bank-related routes
"""
import pytest
from app import db, BankAccount


class TestBankPage:
    """Tests for bank page"""
    
    def test_bank_page_loads(self, authenticated_client):
        """Test that bank page loads"""
        response = authenticated_client.get('/bank')
        assert response.status_code == 200
    
    def test_bank_shows_connected_accounts(self, authenticated_client, test_bank_account):
        """Test that connected bank accounts are displayed"""
        response = authenticated_client.get('/bank')
        assert response.status_code == 200
        assert b'Sparkasse' in response.data or b'bank' in response.data.lower()


class TestConnectBank:
    """Tests for connecting bank accounts"""
    
    def test_connect_bank_success(self, test_app, authenticated_client, test_user):
        """Test successful bank connection"""
        with test_app.app_context():
            response = authenticated_client.post('/bank/connect',
                data={
                    'bank_name': 'Deutsche Bank',
                    'account_number': 'DE98765432109876543210'
                },
                follow_redirects=True
            )
            assert response.status_code == 200
            
            # Verify bank account was created/updated
            bank_account = BankAccount.query.filter_by(
                user_id=test_user['id'],
                bank_name='Deutsche Bank'
            ).first()
            assert bank_account is not None
            assert bank_account.is_connected is True
    
    def test_connect_existing_bank(self, test_app, authenticated_client, test_user, test_bank_account):
        """Test connecting an already connected bank"""
        with test_app.app_context():
            account = BankAccount.query.get(test_bank_account['id'])
            original_account_number = account.account_number
            response = authenticated_client.post('/bank/connect',
                data={
                    'bank_name': 'Sparkasse',
                    'account_number': 'DE11111111111111111111'
                },
                follow_redirects=True
            )
            assert response.status_code == 200
            
            # Verify account was updated
            db.session.refresh(account)
            assert account.account_number == 'DE11111111111111111111'
            assert account.is_connected is True
    
    def test_connect_bank_requires_auth(self, client):
        """Test that connecting bank requires authentication"""
        response = client.post('/bank/connect',
            data={
                'bank_name': 'Test Bank',
                'account_number': 'DE1234567890'
            }
        )
        # Should redirect to login
        assert response.status_code in [302, 401, 403]


class TestBankTransaction:
    """Tests for bank transactions"""
    
    def test_bank_transaction_success(self, authenticated_client):
        """Test successful bank transaction"""
        response = authenticated_client.post('/bank/transaction',
            data={
                'transaction_type': 'debit',
                'amount': '100.00',
                'bank_name': 'Sparkasse'
            },
            follow_redirects=True
        )
        assert response.status_code == 200
        # Should show success message
        assert b'processed' in response.data.lower() or b'success' in response.data.lower()
    
    def test_bank_transaction_requires_auth(self, client):
        """Test that bank transaction requires authentication"""
        response = client.post('/bank/transaction',
            data={
                'transaction_type': 'debit',
                'amount': '100.00',
                'bank_name': 'Sparkasse'
            }
        )
        # Should redirect to login
        assert response.status_code in [302, 401, 403]

