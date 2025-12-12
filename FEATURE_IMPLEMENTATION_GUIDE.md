# Feature Implementation Guide

This document outlines the implementation of advanced features for the SwissAxa Portal.

## ✅ Implemented Features

### 1. Email Integration (`email_service.py`)
- **Status**: ✅ Complete
- **Features**:
  - Flask-Mail integration
  - Send actual emails (not simulated)
  - Claim notification emails
  - Appointment confirmation emails
  - Contact email forwarding

**Setup:**
```bash
# Set environment variables
export MAIL_SERVER=smtp.gmail.com
export MAIL_PORT=587
export MAIL_USE_TLS=True
export MAIL_USERNAME=your-email@gmail.com
export MAIL_PASSWORD=your-app-password
export MAIL_DEFAULT_SENDER=noreply@swissaxa.de
```

### 2. Enhanced AI Features (`ai_services.py`)
- **Status**: ✅ Complete
- **Features**:
  - OpenAI Vision API for image analysis
  - Enhanced document OCR analysis
  - Multi-language AI support (via language parameter)

**Usage:**
```python
# Analyze claim with images
result = AIService.analyze_claim_damage(
    claim_description="Water damage",
    image_files=[open('damage1.jpg', 'rb'), open('damage2.jpg', 'rb')]
)
```

### 3. Multi-Language Support (`i18n_support.py`)
- **Status**: ✅ Complete
- **Features**:
  - German and English support
  - Session-based language selection
  - Flask-Babel integration

**Usage:**
```python
from i18n_support import set_language, get_locale
set_language('de')  # Switch to German
```

### 4. Notifications System (`notifications.py`)
- **Status**: ✅ Complete
- **Features**:
  - In-app notifications
  - Claim status notifications
  - Appointment confirmations
  - Policy update notifications

**Usage:**
```python
from notifications import create_claim_notification
create_claim_notification(user_id, 'CLM-123', 'approved')
```

### 5. Analytics System (`analytics.py`)
- **Status**: ✅ Complete
- **Features**:
  - User activity tracking
  - AI usage analytics
  - Cost tracking
  - Performance metrics

**Usage:**
```python
from analytics import track_event, track_ai_usage
track_event('page_view', 'dashboard', user_id=1)
track_ai_usage('policy_comparison', user_id=1, tokens_used=500)
```

## 🔄 Integration Steps

### Step 1: Update app.py

Add these imports at the top:
```python
from email_service import init_email, send_contact_email, send_claim_notification, send_appointment_confirmation
from notifications import create_claim_notification, create_appointment_notification
from analytics import init_analytics, track_event, track_ai_usage, get_analytics_summary
from i18n_support import init_i18n, set_language
```

Initialize services:
```python
# After db initialization
init_email(app)
init_analytics(db)
init_i18n(app)
```

### Step 2: Update Database Models

Add analytics models to app.py:
```python
from analytics import AnalyticsEvent, AIUsageLog
```

Run migration:
```python
with app.app_context():
    db.create_all()
```

### Step 3: Update Routes

**Contact Route:**
```python
@app.route('/services/contact', methods=['POST'])
@login_required
def contact():
    # ... existing code ...
    if send_contact_email(recipient_email, current_user.first_name, 
                         current_user.email, subject, message):
        flash(f'Email sent to {recipient_email}', 'success')
    else:
        flash('Failed to send email. Please try again.', 'error')
```

**Claims Route:**
```python
@app.route('/services/claims/file', methods=['POST'])
@login_required
def file_claim():
    # ... existing code ...
    # Track event
    track_event('claim_filed', f'Claim {claim.claim_number}', 
                user_id=current_user.id, request=request)
    
    # Send notification
    create_claim_notification(current_user.id, claim.claim_number, 'submitted')
    
    # Send email
    send_claim_notification(current_user.email, claim.claim_number, 'submitted')
```

## 📱 Mobile API Endpoints

### Create `mobile_api.py`:

```python
from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user

mobile_api = Blueprint('mobile_api', __name__, url_prefix='/api/mobile')

@mobile_api.route('/claims', methods=['GET'])
@login_required
def get_claims():
    """Get user claims for mobile app"""
    claims = Claim.query.filter_by(user_id=current_user.id).all()
    return jsonify([{
        'id': c.id,
        'claim_number': c.claim_number,
        'status': c.status,
        'damage_type': c.damage_type,
        'description': c.description
    } for c in claims])

@mobile_api.route('/notifications', methods=['GET'])
@login_required
def get_notifications():
    """Get notifications for mobile app"""
    from notifications import get_user_notifications
    notifications = get_user_notifications(current_user.id)
    return jsonify([n.to_dict() for n in notifications])
```

## 🏦 Bank API Integration Structure

### Create `bank_api_integration.py`:

```python
"""
Bank API Integration Module
Supports Sparkasse, N26, Deutsche Bank APIs
"""
import requests
import os

class BankAPI:
    def __init__(self, bank_name):
        self.bank_name = bank_name
        self.api_key = os.getenv(f'{bank_name.upper()}_API_KEY')
        self.base_url = self._get_base_url(bank_name)
    
    def _get_base_url(self, bank_name):
        """Get API base URL for bank"""
        urls = {
            'sparkasse': 'https://api.sparkasse.de/v1',
            'n26': 'https://api.tech26.de',
            'deutsche_bank': 'https://api.deutsche-bank.de/v1'
        }
        return urls.get(bank_name.lower(), '')
    
    def get_balance(self, account_number):
        """Get account balance"""
        # Implementation would call actual bank API
        # For now, return mock data
        return {'balance': 0.0, 'currency': 'EUR'}
    
    def initiate_transaction(self, from_account, to_account, amount, description):
        """Initiate a transaction"""
        # Implementation would call actual bank API
        return {'transaction_id': 'TXN-123', 'status': 'pending'}
```

## 📊 Advanced Analytics Dashboard

### Create route in app.py:

```python
@app.route('/admin/analytics')
@login_required
def analytics_dashboard():
    """Advanced analytics dashboard"""
    from analytics import get_analytics_summary, get_ai_usage_stats
    
    summary = get_analytics_summary(days=30)
    ai_stats = get_ai_usage_stats(days=30)
    
    return render_template('analytics.html', 
                         summary=summary, 
                         ai_stats=ai_stats)
```

## 🌐 Multi-Language Templates

Update templates to use translations:
```html
<!-- In templates -->
<h1>{{ _('Dashboard') }}</h1>
<p>{{ _('Welcome to SwissAxa Portal') }}</p>
```

## 🔔 Web Push Notifications

Add to base.html:
```html
<script>
// Request notification permission
if ('Notification' in window && Notification.permission === 'default') {
    Notification.requestPermission();
}

// Show notification
function showNotification(title, body, url) {
    if (Notification.permission === 'granted') {
        const notification = new Notification(title, {
            body: body,
            icon: '/static/img/icon.png'
        });
        notification.onclick = () => {
            window.location.href = url;
        };
    }
}
</script>
```

## 📝 Next Steps

1. **Install new dependencies:**
   ```bash
   pip install Flask-Mail Flask-Babel
   ```

2. **Set environment variables** for email and other services

3. **Run database migration** to add analytics tables

4. **Update routes** to use new services

5. **Test each feature** individually

6. **Create mobile app** using the API endpoints

## ⚠️ Notes

- **Bank API Integration**: Requires actual API credentials from banks
- **Mobile App**: Requires separate mobile development (React Native, Flutter, etc.)
- **Email Service**: Requires SMTP server configuration
- **Push Notifications**: Requires HTTPS in production

See individual module files for detailed documentation.

