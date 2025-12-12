"""
Mobile API Endpoints for SwissAxa Portal
Provides REST API for mobile app integration
"""
from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app import db
from datetime import datetime

mobile_api = Blueprint('mobile_api', __name__, url_prefix='/api/mobile')

@mobile_api.route('/claims', methods=['GET'])
@login_required
def get_claims():
    """Get user claims for mobile app"""
    from app import Claim, ClaimMedia
    
    claims = Claim.query.filter_by(user_id=current_user.id).order_by(Claim.created_at.desc()).all()
    
    return jsonify([{
        'id': c.id,
        'claim_number': c.claim_number,
        'status': c.status,
        'damage_type': c.damage_type,
        'description': c.description,
        'address': c.address,
        'created_at': c.created_at.isoformat() if c.created_at else None,
        'media_count': len(c.media) if hasattr(c, 'media') else 0
    } for c in claims])

@mobile_api.route('/claims/<int:claim_id>', methods=['GET'])
@login_required
def get_claim_detail(claim_id):
    """Get detailed claim information"""
    from app import Claim
    
    claim = Claim.query.filter_by(id=claim_id, user_id=current_user.id).first()
    if not claim:
        return jsonify({'error': 'Claim not found'}), 404
    
    return jsonify({
        'id': claim.id,
        'claim_number': claim.claim_number,
        'status': claim.status,
        'damage_type': claim.damage_type,
        'description': claim.description,
        'address': claim.address,
        'latitude': claim.latitude,
        'longitude': claim.longitude,
        'created_at': claim.created_at.isoformat() if claim.created_at else None,
        'media': [{
            'id': m.id,
            'filename': m.filename,
            'media_type': m.media_type
        } for m in claim.media] if hasattr(claim, 'media') else []
    })

@mobile_api.route('/notifications', methods=['GET'])
@login_required
def get_notifications():
    """Get notifications for mobile app"""
    try:
        from notifications import get_user_notifications
        notifications = get_user_notifications(current_user.id)
        return jsonify([n.to_dict() for n in notifications])
    except ImportError:
        return jsonify([])

@mobile_api.route('/notifications/<int:notification_id>/read', methods=['POST'])
@login_required
def mark_notification_read(notification_id):
    """Mark notification as read"""
    try:
        from notifications import mark_notification_read
        mark_notification_read(current_user.id, notification_id)
        return jsonify({'success': True})
    except ImportError:
        return jsonify({'error': 'Notifications not available'}), 500

@mobile_api.route('/policies', methods=['GET'])
@login_required
def get_policies():
    """Get user policies for mobile app"""
    from app import SwissAxaPolicy
    
    policies = SwissAxaPolicy.query.filter_by(user_id=current_user.id).all()
    
    return jsonify([{
        'id': p.id,
        'policy_number': p.policy_number,
        'policy_type': p.policy_type,
        'coverage_amount': float(p.coverage_amount),
        'premium': float(p.premium),
        'status': p.status,
        'expiration_date': p.expiration_date.isoformat() if p.expiration_date else None
    } for p in policies])

@mobile_api.route('/documents', methods=['GET'])
@login_required
def get_documents():
    """Get user documents for mobile app"""
    from app import Document
    
    documents = Document.query.filter_by(user_id=current_user.id).order_by(Document.uploaded_at.desc()).all()
    
    return jsonify([{
        'id': d.id,
        'filename': d.filename,
        'document_type': d.document_type,
        'uploaded_at': d.uploaded_at.isoformat() if d.uploaded_at else None
    } for d in documents])

@mobile_api.route('/dashboard/stats', methods=['GET'])
@login_required
def get_dashboard_stats():
    """Get dashboard statistics for mobile app"""
    from app import Claim, SwissAxaPolicy, Document, Appointment
    
    stats = {
        'total_policies': SwissAxaPolicy.query.filter_by(user_id=current_user.id).count(),
        'active_claims': Claim.query.filter_by(user_id=current_user.id, status='submitted').count(),
        'total_documents': Document.query.filter_by(user_id=current_user.id).count(),
        'upcoming_appointments': Appointment.query.filter_by(
            user_id=current_user.id,
            status='scheduled'
        ).filter(Appointment.date_time > datetime.utcnow()).count()
    }
    
    return jsonify(stats)

@mobile_api.route('/chat', methods=['POST'])
@login_required
def mobile_chat():
    """Mobile chat endpoint"""
    from ai_services import AIService
    
    message = request.json.get('message', '')
    if not message:
        return jsonify({'error': 'Message required'}), 400
    
    # Get conversation history from session
    conversation_history = request.json.get('history', [])
    
    # Get AI response
    response = AIService.chat_with_ai(message, conversation_history)
    
    return jsonify({
        'response': response,
        'timestamp': datetime.utcnow().isoformat()
    })

