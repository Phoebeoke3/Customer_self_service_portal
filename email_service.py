"""
Email Service Module for SwissAxa Portal
Handles email sending using Flask-Mail
"""
from flask import current_app
from flask_mail import Mail, Message
import os

mail = Mail()

def init_email(app):
    """Initialize email service with Flask app"""
    # Email configuration
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'
    app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL', 'False').lower() == 'true'
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME', '')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD', '')
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER', 'noreply@swissaxa.de')
    
    mail.init_app(app)
    return mail

def send_email(to, subject, body, html_body=None, attachments=None):
    """
    Send an email
    
    Args:
        to: Recipient email address or list of addresses
        subject: Email subject
        body: Plain text body
        html_body: HTML body (optional)
        attachments: List of attachment file paths (optional)
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        msg = Message(
            subject=subject,
            recipients=[to] if isinstance(to, str) else to,
            body=body,
            html=html_body
        )
        
        # Add attachments if provided
        if attachments:
            for attachment_path in attachments:
                if os.path.exists(attachment_path):
                    with current_app.open_resource(attachment_path) as f:
                        msg.attach(
                            os.path.basename(attachment_path),
                            'application/octet-stream',
                            f.read()
                        )
        
        mail.send(msg)
        return True
    except Exception as e:
        current_app.logger.error(f"Failed to send email: {e}")
        return False

def send_claim_notification(user_email, claim_number, status):
    """Send notification email for claim status updates"""
    subject = f"Claim Update: {claim_number}"
    body = f"""
Dear Customer,

Your claim {claim_number} status has been updated to: {status}

You can view the details in your customer portal.

Best regards,
SwissAxa Customer Service
"""
    html_body = f"""
    <html>
    <body>
        <h2>Claim Update</h2>
        <p>Dear Customer,</p>
        <p>Your claim <strong>{claim_number}</strong> status has been updated to: <strong>{status}</strong></p>
        <p>You can view the details in your <a href="http://localhost:5000/services/claims">customer portal</a>.</p>
        <p>Best regards,<br>SwissAxa Customer Service</p>
    </body>
    </html>
    """
    return send_email(user_email, subject, body, html_body)

def send_appointment_confirmation(user_email, appointment_date, agent_name=None):
    """Send appointment confirmation email"""
    agent_info = f" with {agent_name}" if agent_name else ""
    subject = "Appointment Confirmation - SwissAxa"
    body = f"""
Dear Customer,

Your appointment{agent_info} has been confirmed for:
{appointment_date}

We look forward to meeting with you.

Best regards,
SwissAxa Customer Service
"""
    html_body = f"""
    <html>
    <body>
        <h2>Appointment Confirmation</h2>
        <p>Dear Customer,</p>
        <p>Your appointment{agent_info} has been confirmed for:</p>
        <p><strong>{appointment_date}</strong></p>
        <p>We look forward to meeting with you.</p>
        <p>Best regards,<br>SwissAxa Customer Service</p>
    </body>
    </html>
    """
    return send_email(user_email, subject, body, html_body)

def send_contact_email(recipient_email, sender_name, sender_email, subject, message):
    """Send contact email from customer to service desk/agent"""
    email_subject = f"Portal Contact: {subject}"
    body = f"""
Message from SwissAxa Customer Portal

From: {sender_name} ({sender_email})
Subject: {subject}

Message:
{message}

---
This email was sent from the SwissAxa Customer Self-Service Portal.
"""
    html_body = f"""
    <html>
    <body>
        <h2>Message from SwissAxa Customer Portal</h2>
        <p><strong>From:</strong> {sender_name} ({sender_email})<br>
        <strong>Subject:</strong> {subject}</p>
        <hr>
        <p>{message.replace(chr(10), '<br>')}</p>
        <hr>
        <p><small>This email was sent from the SwissAxa Customer Self-Service Portal.</small></p>
    </body>
    </html>
    """
    return send_email(recipient_email, email_subject, body, html_body)

