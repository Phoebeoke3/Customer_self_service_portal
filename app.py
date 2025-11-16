from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import os
import json
from pathlib import Path

app = Flask(__name__)
app.config['SECRET_KEY'] = 'swissaxa-secret-key-2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///swissaxa_portal.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create upload directories
os.makedirs('uploads/documents', exist_ok=True)
os.makedirs('uploads/policies', exist_ok=True)
os.makedirs('uploads/claims', exist_ok=True)

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    address = db.Column(db.String(255))
    correspondence_address = db.Column(db.String(255))
    bank_account = db.Column(db.String(50))
    agent_id = db.Column(db.Integer, db.ForeignKey('agent.id'))
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Agent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))

class SwissAxaPolicy(db.Model):
    __tablename__ = 'swissaxa_policy'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    policy_number = db.Column(db.String(50), unique=True, nullable=False)
    policy_type = db.Column(db.String(100))
    coverage_amount = db.Column(db.Float)
    premium = db.Column(db.Float)
    expiration_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='swissaxa_policies')

class ExternalPolicy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    insurance_company = db.Column(db.String(100), nullable=False)
    policy_number = db.Column(db.String(50))
    policy_type = db.Column(db.String(100))
    expiration_date = db.Column(db.Date)
    file_path = db.Column(db.String(255))
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='external_policies')

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    document_type = db.Column(db.String(100))
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='documents')

class Claim(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    policy_id = db.Column(db.Integer, db.ForeignKey('swissaxa_policy.id'))
    claim_number = db.Column(db.String(50), unique=True)
    description = db.Column(db.Text)
    damage_type = db.Column(db.String(100))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    address = db.Column(db.String(255))
    status = db.Column(db.String(20), default='submitted')
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='claims')
    policy = db.relationship('SwissAxaPolicy', backref='claims')

class ClaimMedia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    claim_id = db.Column(db.Integer, db.ForeignKey('claim.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    media_type = db.Column(db.String(20))  # 'photo' or 'video'
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    claim = db.relationship('Claim', backref='media')

class PolicyChangeRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    policy_id = db.Column(db.Integer, db.ForeignKey('swissaxa_policy.id'))
    request_type = db.Column(db.String(50))  # 'upgrade', 'change', 'cancel'
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='policy_change_requests')
    policy = db.relationship('SwissAxaPolicy', backref='change_requests')

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    agent_id = db.Column(db.Integer, db.ForeignKey('agent.id'))
    appointment_type = db.Column(db.String(50))  # 'service_desk' or 'agent'
    date_time = db.Column(db.DateTime, nullable=False)
    purpose = db.Column(db.Text)
    status = db.Column(db.String(20), default='scheduled')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='appointments')
    agent = db.relationship('Agent', backref='appointments')

class BankAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    bank_name = db.Column(db.String(100), nullable=False)  # Sparkasse, N26, Deutsche Bank, etc.
    account_number = db.Column(db.String(50))
    is_connected = db.Column(db.Boolean, default=False)
    
    user = db.relationship('User', backref='bank_accounts')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return render_template('register.html')
        
        user = User(email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

# Policies routes
@app.route('/policies')
@login_required
def policies():
    swissaxa_policies = SwissAxaPolicy.query.filter_by(user_id=current_user.id).all()
    external_policies = ExternalPolicy.query.filter_by(user_id=current_user.id).all()
    
    # Calculate days until expiry for each policy
    today = datetime.now().date()
    for policy in swissaxa_policies:
        if policy.expiration_date:
            days_until_expiry = (policy.expiration_date - today).days
            policy.days_until_expiry = days_until_expiry
        else:
            policy.days_until_expiry = 999
    
    return render_template('policies.html', 
                         swissaxa_policies=swissaxa_policies,
                         external_policies=external_policies,
                         today=today)

@app.route('/policies/external/upload', methods=['POST'])
@login_required
def upload_external_policy():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'policies', filename)
        file.save(filepath)
        
        external_policy = ExternalPolicy(
            user_id=current_user.id,
            insurance_company=request.form.get('insurance_company', 'Unknown'),
            policy_number=request.form.get('policy_number', ''),
            policy_type=request.form.get('policy_type', ''),
            expiration_date=datetime.strptime(request.form.get('expiration_date'), '%Y-%m-%d').date() if request.form.get('expiration_date') else None,
            file_path=filepath
        )
        db.session.add(external_policy)
        db.session.commit()
        
        flash('External policy uploaded successfully', 'success')
        return jsonify({'success': True})

# Documents routes
@app.route('/documents')
@login_required
def documents():
    user_documents = Document.query.filter_by(user_id=current_user.id).all()
    return render_template('documents.html', documents=user_documents)

@app.route('/documents/upload', methods=['POST'])
@login_required
def upload_document():
    if 'file' not in request.files:
        flash('No file provided', 'error')
        return redirect(url_for('documents'))
    
    file = request.files['file']
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('documents'))
    
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'documents', filename)
        file.save(filepath)
        
        document = Document(
            user_id=current_user.id,
            filename=filename,
            file_path=filepath,
            document_type=request.form.get('document_type', 'general')
        )
        db.session.add(document)
        db.session.commit()
        
        flash('Document uploaded successfully', 'success')
        return redirect(url_for('documents'))

@app.route('/documents/download/<int:doc_id>')
@login_required
def download_document(doc_id):
    document = Document.query.get_or_404(doc_id)
    if document.user_id != current_user.id:
        flash('Unauthorized access', 'error')
        return redirect(url_for('documents'))
    
    return send_file(document.file_path, as_attachment=True, download_name=document.filename)

# Bank routes
@app.route('/bank')
@login_required
def bank():
    bank_accounts = BankAccount.query.filter_by(user_id=current_user.id).all()
    return render_template('bank.html', bank_accounts=bank_accounts)

@app.route('/bank/connect', methods=['POST'])
@login_required
def connect_bank():
    bank_name = request.form.get('bank_name')
    account_number = request.form.get('account_number')
    
    bank_account = BankAccount.query.filter_by(
        user_id=current_user.id,
        bank_name=bank_name
    ).first()
    
    if not bank_account:
        bank_account = BankAccount(
            user_id=current_user.id,
            bank_name=bank_name,
            account_number=account_number,
            is_connected=True
        )
        db.session.add(bank_account)
    else:
        bank_account.is_connected = True
        bank_account.account_number = account_number
    
    db.session.commit()
    flash(f'Connected to {bank_name} successfully', 'success')
    return redirect(url_for('bank'))

@app.route('/bank/transaction', methods=['POST'])
@login_required
def bank_transaction():
    # Simulated transaction - in production, this would integrate with bank APIs
    transaction_type = request.form.get('transaction_type')
    amount = request.form.get('amount')
    bank_name = request.form.get('bank_name')
    
    flash(f'Transaction {transaction_type} of {amount} EUR processed via {bank_name}', 'success')
    return redirect(url_for('bank'))

# Services routes
@app.route('/services')
@login_required
def services():
    return render_template('services.html')

@app.route('/services/claims')
@login_required
def claims():
    user_claims = Claim.query.filter_by(user_id=current_user.id).all()
    policies = SwissAxaPolicy.query.filter_by(user_id=current_user.id).all()
    return render_template('claims.html', claims=user_claims, policies=policies)

@app.route('/services/claims/file', methods=['POST'])
@login_required
def file_claim():
    claim = Claim(
        user_id=current_user.id,
        policy_id=request.form.get('policy_id') if request.form.get('policy_id') else None,
        claim_number=f'CLM-{datetime.now().strftime("%Y%m%d%H%M%S")}',
        description=request.form.get('description'),
        damage_type=request.form.get('damage_type'),
        latitude=float(request.form.get('latitude')) if request.form.get('latitude') else None,
        longitude=float(request.form.get('longitude')) if request.form.get('longitude') else None,
        address=request.form.get('address')
    )
    db.session.add(claim)
    db.session.flush()
    
    # Handle media uploads
    if 'media' in request.files:
        files = request.files.getlist('media')
        for file in files:
            if file.filename:
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'claims', filename)
                file.save(filepath)
                
                media_type = 'video' if filename.lower().endswith(('.mp4', '.avi', '.mov')) else 'photo'
                claim_media = ClaimMedia(
                    claim_id=claim.id,
                    filename=filename,
                    file_path=filepath,
                    media_type=media_type
                )
                db.session.add(claim_media)
    
    db.session.commit()
    flash('Claim filed successfully', 'success')
    return redirect(url_for('claims'))

@app.route('/services/policy-management')
@login_required
def policy_management():
    policies = SwissAxaPolicy.query.filter_by(user_id=current_user.id).all()
    change_requests = PolicyChangeRequest.query.filter_by(user_id=current_user.id).all()
    return render_template('policy_management.html', policies=policies, change_requests=change_requests)

@app.route('/services/policy-management/request', methods=['POST'])
@login_required
def submit_policy_change():
    change_request = PolicyChangeRequest(
        user_id=current_user.id,
        policy_id=request.form.get('policy_id') if request.form.get('policy_id') else None,
        request_type=request.form.get('request_type'),
        description=request.form.get('description')
    )
    db.session.add(change_request)
    db.session.commit()
    flash('Policy change request submitted successfully', 'success')
    return redirect(url_for('policy_management'))

@app.route('/services/contact', methods=['GET', 'POST'])
@login_required
def contact():
    agents = Agent.query.all()
    if request.method == 'POST':
        recipient_type = request.form.get('recipient_type')
        recipient_email = request.form.get('recipient_email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        
        # In production, this would send actual emails
        flash(f'Email sent to {recipient_email}', 'success')
        return redirect(url_for('contact'))
    
    return render_template('contact.html', agents=agents)

@app.route('/services/scheduling', methods=['GET', 'POST'])
@login_required
def scheduling():
    agents = Agent.query.all()
    appointments = Appointment.query.filter_by(user_id=current_user.id).all()
    
    if request.method == 'POST':
        appointment = Appointment(
            user_id=current_user.id,
            agent_id=request.form.get('agent_id') if request.form.get('agent_id') else None,
            appointment_type=request.form.get('appointment_type'),
            date_time=datetime.strptime(request.form.get('date_time'), '%Y-%m-%dT%H:%M'),
            purpose=request.form.get('purpose')
        )
        db.session.add(appointment)
        db.session.commit()
        flash('Appointment booked successfully', 'success')
        return redirect(url_for('scheduling'))
    
    return render_template('scheduling.html', agents=agents, appointments=appointments)

# Information routes
@app.route('/information')
@login_required
def information():
    return render_template('information.html', user=current_user)

@app.route('/information/update', methods=['POST'])
@login_required
def update_information():
    current_user.first_name = request.form.get('first_name')
    current_user.last_name = request.form.get('last_name')
    current_user.phone = request.form.get('phone')
    current_user.address = request.form.get('address')
    current_user.correspondence_address = request.form.get('correspondence_address')
    current_user.bank_account = request.form.get('bank_account')
    
    db.session.commit()
    flash('Information updated successfully', 'success')
    return redirect(url_for('information'))

# AI-powered external policy comparison
@app.route('/api/policy-comparison', methods=['POST'])
@login_required
def compare_policies():
    # Simplified AI comparison - in production, use OpenAI or similar
    external_policy_data = request.json.get('external_policy')
    
    # Mock AI comparison result
    comparison_result = {
        'similar_products': [
            {
                'name': 'Comprehensive Insurance Premium',
                'coverage': external_policy_data.get('policy_type', 'General'),
                'premium': '99.99 EUR/month',
                'match_score': 85
            }
        ],
        'recommendations': [
            'Our premium product offers 20% better coverage',
            'Includes 24/7 customer support',
            'Faster claims processing'
        ]
    }
    
    return jsonify(comparison_result)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Create sample agent
        if not Agent.query.first():
            agent = Agent(name='Max Müller', email='max.mueller@swissaxa.de', phone='+49 221 123456')
            db.session.add(agent)
            db.session.commit()
    app.run(debug=True, host='127.0.0.1', port=5000)

