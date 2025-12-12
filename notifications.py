"""
Notifications Module for SwissAxa Portal
Handles web push notifications and in-app notifications
"""
from flask import session
from datetime import datetime
import json

class Notification:
    """Notification model"""
    def __init__(self, notification_id, title, message, notification_type='info', 
                 action_url=None, timestamp=None, read=False):
        self.id = notification_id
        self.title = title
        self.message = message
        self.type = notification_type  # 'info', 'success', 'warning', 'error'
        self.action_url = action_url
        self.timestamp = timestamp or datetime.utcnow()
        self.read = read
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'message': self.message,
            'type': self.type,
            'action_url': self.action_url,
            'timestamp': self.timestamp.isoformat() if isinstance(self.timestamp, datetime) else str(self.timestamp),
            'read': self.read
        }

def get_user_notifications(user_id):
    """Get notifications for a user (stored in session for demo)"""
    key = f'notifications_{user_id}'
    notifications_data = session.get(key, [])
    return [Notification(**n) if isinstance(n, dict) else n for n in notifications_data]

def add_notification(user_id, title, message, notification_type='info', action_url=None):
    """Add a notification for a user"""
    key = f'notifications_{user_id}'
    notifications = get_user_notifications(user_id)
    
    notification_id = len(notifications) + 1
    notification = Notification(
        notification_id=notification_id,
        title=title,
        message=message,
        notification_type=notification_type,
        action_url=action_url
    )
    
    notifications.insert(0, notification)  # Add to beginning
    # Keep only last 50 notifications
    notifications = notifications[:50]
    
    session[key] = [n.to_dict() for n in notifications]
    return notification

def mark_notification_read(user_id, notification_id):
    """Mark a notification as read"""
    notifications = get_user_notifications(user_id)
    for notification in notifications:
        if notification.id == notification_id:
            notification.read = True
            break
    
    key = f'notifications_{user_id}'
    session[key] = [n.to_dict() for n in notifications]

def mark_all_read(user_id):
    """Mark all notifications as read"""
    notifications = get_user_notifications(user_id)
    for notification in notifications:
        notification.read = True
    
    key = f'notifications_{user_id}'
    session[key] = [n.to_dict() for n in notifications]

def create_claim_notification(user_id, claim_number, status):
    """Create notification for claim status update"""
    return add_notification(
        user_id=user_id,
        title=f"Claim {claim_number} Updated",
        message=f"Your claim status has been updated to: {status}",
        notification_type='info',
        action_url=f'/services/claims'
    )

def create_appointment_notification(user_id, appointment_date, agent_name=None):
    """Create notification for appointment confirmation"""
    agent_text = f" with {agent_name}" if agent_name else ""
    return add_notification(
        user_id=user_id,
        title="Appointment Confirmed",
        message=f"Your appointment{agent_text} is confirmed for {appointment_date}",
        notification_type='success',
        action_url='/services/scheduling'
    )

def create_policy_notification(user_id, policy_number, message):
    """Create notification for policy updates"""
    return add_notification(
        user_id=user_id,
        title=f"Policy {policy_number} Update",
        message=message,
        notification_type='info',
        action_url='/policies'
    )

