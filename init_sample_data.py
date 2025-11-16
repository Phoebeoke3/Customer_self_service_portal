"""
Script to initialize sample data for SwissAxa Customer Portal
Run this after setting up the database to create sample policies and data
"""

from app import app, db, User, Agent, SwissAxaPolicy, ExternalPolicy
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash

def init_sample_data():
    with app.app_context():
        # Create sample user if doesn't exist
        user = User.query.filter_by(email='demo@example.com').first()
        if not user:
            user = User(
                email='demo@example.com',
                first_name='Max',
                last_name='Mustermann',
                phone='+49 221 1234567',
                address='Musterstraße 123, 50667 Köln, NRW',
                correspondence_address='Musterstraße 123, 50667 Köln, NRW',
                bank_account='DE89 3704 0044 0532 0130 00'
            )
            user.set_password('demo123')
            db.session.add(user)
            db.session.commit()
            print(f"Created demo user: {user.email}")
        else:
            print(f"Demo user already exists: {user.email}")

        # Create sample agent if doesn't exist
        agent = Agent.query.filter_by(email='max.mueller@swissaxa.de').first()
        if not agent:
            agent = Agent(
                name='Max Müller',
                email='max.mueller@swissaxa.de',
                phone='+49 221 123456'
            )
            db.session.add(agent)
            db.session.commit()
            print(f"Created sample agent: {agent.name}")
        else:
            print(f"Sample agent already exists: {agent.name}")

        # Create sample SwissAxa policies
        existing_policies = SwissAxaPolicy.query.filter_by(user_id=user.id).count()
        if existing_policies == 0:
            policies = [
                SwissAxaPolicy(
                    user_id=user.id,
                    policy_number='SAX-2024-001',
                    policy_type='Comprehensive Auto Insurance',
                    coverage_amount=50000.00,
                    premium=1200.00,
                    expiration_date=datetime.now().date() + timedelta(days=45),
                    status='active'
                ),
                SwissAxaPolicy(
                    user_id=user.id,
                    policy_number='SAX-2024-002',
                    policy_type='Home Insurance',
                    coverage_amount=250000.00,
                    premium=850.00,
                    expiration_date=datetime.now().date() + timedelta(days=120),
                    status='active'
                ),
                SwissAxaPolicy(
                    user_id=user.id,
                    policy_number='SAX-2023-005',
                    policy_type='Health Insurance',
                    coverage_amount=100000.00,
                    premium=4500.00,
                    expiration_date=datetime.now().date() - timedelta(days=15),
                    status='expired'
                )
            ]
            for policy in policies:
                db.session.add(policy)
            db.session.commit()
            print(f"Created {len(policies)} sample SwissAxa policies")
        else:
            print(f"Sample policies already exist ({existing_policies} policies)")

        # Create sample external policy
        existing_external = ExternalPolicy.query.filter_by(user_id=user.id).count()
        if existing_external == 0:
            external_policy = ExternalPolicy(
                user_id=user.id,
                insurance_company='Allianz',
                policy_number='ALL-2024-123',
                policy_type='Life Insurance',
                expiration_date=datetime.now().date() + timedelta(days=180),
                file_path='uploads/policies/sample_policy.pdf'
            )
            db.session.add(external_policy)
            db.session.commit()
            print("Created sample external policy")
        else:
            print(f"Sample external policies already exist ({existing_external} policies)")

        print("\nSample data initialization complete!")
        print("\nLogin credentials:")
        print("Email: demo@example.com")
        print("Password: demo123")

if __name__ == '__main__':
    init_sample_data()

