from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import os
import json
from pathlib import Path

# Try to import AI services (will work if OpenAI is configured)
try:
    from ai_services import AIService
    AI_AVAILABLE = True
except (ImportError, Exception) as e:
    AI_AVAILABLE = False
    # Create a mock AIService class
    class AIService:
        @staticmethod
        def is_available():
            return False
        @staticmethod
        def compare_policies(data):
            return {'similar_products': [], 'recommendations': []}
        @staticmethod
        def tag_document(filename):
            return 'general'
        @staticmethod
        def analyze_claim_damage(**kwargs):
            return {}
        @staticmethod
        def recommend_policies(profile):
            return []
        @staticmethod
        def suggest_appointment_times(user_id, appointment_type):
            return []
        @staticmethod
        def detect_transaction_anomaly(transactions):
            return {'is_anomaly': False}
        @staticmethod
        def validate_user_data(data):
            return {'is_valid': True, 'inconsistencies': []}
        @staticmethod
        def chat_with_ai(message, history=None):
            return "AI services are currently unavailable. Please contact customer service."

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
        
        # AI-powered document tagging
        document_type = request.form.get('document_type')
        if not document_type or document_type == 'auto':
            # Use AI to auto-tag the document
            ai_tag = AIService.tag_document(filename)
            document_type = ai_tag
            flash(f'Document automatically tagged as: {ai_tag.replace("_", " ").title()}', 'info')
        
        document = Document(
            user_id=current_user.id,
            filename=filename,
            file_path=filepath,
            document_type=document_type or 'general'
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
    description = request.form.get('description', '')
    damage_type = request.form.get('damage_type', '')
    
    # AI-powered claims analysis if media is uploaded
    ai_analysis = None
    if 'media' in request.files:
        files = request.files.getlist('media')
        if files and files[0].filename:
            # Perform AI analysis on the claim
            ai_analysis = AIService.analyze_claim_damage(
                claim_description=description
            )
            
            # Use AI suggestions only if user hasn't provided values
            # User-provided values take precedence
            if ai_analysis.get('damage_type') and not damage_type:
                damage_type = ai_analysis.get('damage_type', damage_type)
            if ai_analysis.get('suggested_description') and not description:
                description = ai_analysis.get('suggested_description', description)
            
            # Set priority based on AI analysis
            priority = ai_analysis.get('priority', 'normal')
    
    # Validate that at least one piece of evidence exists
    has_evidence = False
    if 'media' in request.files:
        files = request.files.getlist('media')
        has_evidence = any(f.filename for f in files)
    
    if not has_evidence:
        flash('Please upload at least one photo or video as evidence', 'error')
        return redirect(url_for('claims'))
    
    claim = Claim(
        user_id=current_user.id,
        policy_id=request.form.get('policy_id') if request.form.get('policy_id') else None,
        claim_number=f'CLM-{datetime.now().strftime("%Y%m%d%H%M%S")}',
        description=description,
        damage_type=damage_type,
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
    
    if ai_analysis:
        flash(f'Claim filed successfully. AI Analysis: {damage_type} detected (Priority: {ai_analysis.get("priority", "normal")})', 'success')
    else:
        flash('Claim filed successfully', 'success')
    return redirect(url_for('claims'))

@app.route('/services/policy-management')
@login_required
def policy_management():
    policies = SwissAxaPolicy.query.filter_by(user_id=current_user.id).all()
    change_requests = PolicyChangeRequest.query.filter_by(user_id=current_user.id).all()
    
    # Get AI recommendations if available
    ai_recommendations = []
    if AIService.is_available():
        user_profile = {
            'policies': [p.policy_type for p in policies],
            'claims_count': len(current_user.claims),
            'location': current_user.address or 'Unknown'
        }
        ai_recommendations = AIService.recommend_policies(user_profile)
    
    return render_template('policy_management.html', 
                         policies=policies, 
                         change_requests=change_requests,
                         ai_recommendations=ai_recommendations)

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
        
        # Send actual email using email service
        try:
            from email_service import send_contact_email
            if send_contact_email(
                recipient_email=recipient_email,
                sender_name=f"{current_user.first_name} {current_user.last_name}",
                sender_email=current_user.email,
                subject=subject,
                message=message
            ):
                flash(f'Email sent to {recipient_email}', 'success')
            else:
                flash('Email service is not configured. Please contact support directly.', 'warning')
        except ImportError:
            # Fallback if email service not available
            flash(f'Email would be sent to {recipient_email} (email service not configured)', 'info')
        
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
        
        # Send notifications
        try:
            from notifications import create_appointment_notification
            agent_name = appointment.agent.name if appointment.agent else None
            create_appointment_notification(
                current_user.id, 
                appointment.date_time.strftime('%Y-%m-%d %H:%M'),
                agent_name
            )
        except ImportError:
            pass
        
        # Send email confirmation
        try:
            from email_service import send_appointment_confirmation
            agent_name = appointment.agent.name if appointment.agent else None
            send_appointment_confirmation(
                current_user.email,
                appointment.date_time.strftime('%Y-%m-%d %H:%M'),
                agent_name
            )
        except ImportError:
            pass
        
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
    # Collect user data for AI validation
    user_data = {
        'first_name': request.form.get('first_name'),
        'last_name': request.form.get('last_name'),
        'phone': request.form.get('phone'),
        'address': request.form.get('address'),
        'correspondence_address': request.form.get('correspondence_address'),
        'email': current_user.email
    }
    
    # AI-powered data validation
    validation_result = AIService.validate_user_data(user_data)
    
    # Check if sensitive fields changed (address, bank account)
    sensitive_changed = (
        current_user.address != request.form.get('address') or
        current_user.correspondence_address != request.form.get('correspondence_address') or
        current_user.bank_account != request.form.get('bank_account')
    )
    
    # Require re-authentication for sensitive changes or if AI detects inconsistencies
    if sensitive_changed or validation_result.get('requires_reauth'):
        # In production, this would require password confirmation
        if validation_result.get('inconsistencies'):
            flash(f'Please verify your information: {", ".join(validation_result["inconsistencies"])}', 'warning')
    
    current_user.first_name = request.form.get('first_name')
    current_user.last_name = request.form.get('last_name')
    current_user.phone = request.form.get('phone')
    current_user.address = request.form.get('address')
    current_user.correspondence_address = request.form.get('correspondence_address')
    current_user.bank_account = request.form.get('bank_account')
    
    db.session.commit()
    
    if validation_result.get('inconsistencies'):
        flash('Information updated. Please review any warnings above.', 'warning')
    else:
        flash('Information updated successfully', 'success')
    return redirect(url_for('information'))

# AI-powered external policy comparison
@app.route('/api/policy-comparison', methods=['POST'])
@login_required
def compare_policies():
    """AI-powered policy comparison using OpenAI"""
    external_policy_data = request.json.get('external_policy', {})
    
    # Use AI service for comparison
    comparison_result = AIService.compare_policies(external_policy_data)
    
    return jsonify(comparison_result)

# AI-powered document tagging
@app.route('/api/document-tag', methods=['POST'])
@login_required
def tag_document():
    """AI-powered document type tagging"""
    filename = request.json.get('filename', '')
    if not filename:
        return jsonify({'error': 'Filename required'}), 400
    
    tag = AIService.tag_document(filename)
    return jsonify({'document_type': tag})

# AI-powered claims analysis
@app.route('/api/claims/analyze', methods=['POST'])
@login_required
def analyze_claim():
    """AI-powered claim damage analysis"""
    data = request.json
    claim_description = data.get('description', '')
    image_description = data.get('image_description', '')
    
    analysis = AIService.analyze_claim_damage(
        image_description=image_description,
        claim_description=claim_description
    )
    
    return jsonify(analysis)

# AI-powered policy recommendations
@app.route('/api/policy-recommendations', methods=['GET'])
@login_required
def get_policy_recommendations():
    """Get AI-powered policy recommendations for user"""
    user_profile = {
        'policies': [p.policy_type for p in current_user.swissaxa_policies],
        'claims_count': len(current_user.claims),
        'location': current_user.address or 'Unknown',
        'age': 'Unknown'  # Could be added to user model
    }
    
    recommendations = AIService.recommend_policies(user_profile)
    return jsonify({'recommendations': recommendations})

# AI-powered appointment suggestions
@app.route('/api/appointment-suggestions', methods=['POST'])
@login_required
def get_appointment_suggestions():
    """Get AI-powered appointment time suggestions"""
    appointment_type = request.json.get('appointment_type', 'service_desk')
    
    suggestions = AIService.suggest_appointment_times(
        user_id=current_user.id,
        appointment_type=appointment_type
    )
    
    return jsonify({'suggestions': suggestions})

# AI chatbot endpoint
@app.route('/api/chat', methods=['POST'])
@login_required
def chat_with_ai():
    """AI chatbot endpoint"""
    message = request.json.get('message', '')
    if not message:
        return jsonify({'error': 'Message required'}), 400
    
    # Get conversation history from session
    conversation_history = session.get('chat_history', [])
    
    # Get AI response
    response = AIService.chat_with_ai(message, conversation_history)
    
    # Update conversation history
    conversation_history.append({'role': 'user', 'content': message})
    conversation_history.append({'role': 'assistant', 'content': response})
    session['chat_history'] = conversation_history[-10:]  # Keep last 10 messages
    
    return jsonify({'response': response})

# Clear chat history
@app.route('/api/chat/clear', methods=['POST'])
@login_required
def clear_chat_history():
    """Clear chat conversation history"""
    session.pop('chat_history', None)
    return jsonify({'success': True})

# Register mobile API blueprint
try:
    from mobile_api import mobile_api
    app.register_blueprint(mobile_api)
except ImportError:
    pass

# Initialize additional services
try:
    from email_service import init_email
    init_email(app)
except ImportError:
    pass

try:
    from analytics import init_analytics
    init_analytics(db)
except ImportError:
    pass

try:
    from i18n_support import init_i18n
    init_i18n(app)
except ImportError:
    pass

# Analytics dashboard route
@app.route('/admin/analytics')
@login_required
def analytics_dashboard():
    """Advanced analytics dashboard"""
    try:
        from analytics import get_analytics_summary, get_ai_usage_stats
        summary = get_analytics_summary(days=30)
        ai_stats = get_ai_usage_stats(days=30)
        return render_template('analytics.html', summary=summary, ai_stats=ai_stats)
    except ImportError:
        flash('Analytics module not available', 'warning')
        return redirect(url_for('dashboard'))

# Language switching route
@app.route('/api/language/<language_code>', methods=['POST'])
@login_required
def set_language(language_code):
    """Set user language preference"""
    try:
        from i18n_support import set_language as set_user_language
        if set_user_language(language_code):
            return jsonify({'success': True, 'language': language_code})
        return jsonify({'error': 'Invalid language code'}), 400
    except ImportError:
        return jsonify({'error': 'i18n not available'}), 500

# Notifications API
@app.route('/api/notifications', methods=['GET'])
@login_required
def get_notifications():
    """Get user notifications"""
    try:
        from notifications import get_user_notifications
        notifications = get_user_notifications(current_user.id)
        return jsonify([n.to_dict() for n in notifications])
    except ImportError:
        return jsonify([])

@app.route('/api/notifications/<int:notification_id>/read', methods=['POST'])
@login_required
def mark_notification_read(notification_id):
    """Mark notification as read"""
    try:
        from notifications import mark_notification_read
        mark_notification_read(current_user.id, notification_id)
        return jsonify({'success': True})
    except ImportError:
        return jsonify({'error': 'Notifications not available'}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Create sample agent
        if not Agent.query.first():
            agent = Agent(name='Max Müller', email='max.mueller@swissaxa.de', phone='+49 221 123456')
            db.session.add(agent)
            db.session.commit()
        
        # Create analytics tables
        try:
            from analytics import AnalyticsEvent, AIUsageLog
            db.create_all()
        except ImportError:
            pass
    app.run(debug=True, host='0.0.0.0', port=5000)

