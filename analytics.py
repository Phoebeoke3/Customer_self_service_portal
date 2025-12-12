"""
Analytics Module for SwissAxa Portal
Tracks user activity, AI usage, and provides insights
"""
from datetime import datetime, timedelta
from sqlalchemy import func
from flask_sqlalchemy import SQLAlchemy
import json

# db will be set by init_analytics
db = None

def init_analytics(app_db):
    """Initialize analytics with database instance"""
    global db, AnalyticsEvent, AIUsageLog
    db = app_db
    AnalyticsEvent, AIUsageLog = _create_models(app_db)
    # Create tables
    try:
        with app_db.app.app_context():
            app_db.create_all()
    except:
        pass

class AnalyticsEvent:
    """Analytics Event Model - will be bound to db in init"""
    pass

class AIUsageLog:
    """AI Usage Log Model - will be bound to db in init"""
    pass

def _create_models(db_instance):
    """Create model classes bound to db"""
    global AnalyticsEvent, AIUsageLog
    
    class AnalyticsEvent(db_instance.Model):
        """Track analytics events"""
        __tablename__ = 'analytics_events'
        
        id = db_instance.Column(db_instance.Integer, primary_key=True)
        user_id = db_instance.Column(db_instance.Integer, db_instance.ForeignKey('user.id'), nullable=True)
        event_type = db_instance.Column(db_instance.String(100), nullable=False)
        event_name = db_instance.Column(db_instance.String(200), nullable=False)
        event_metadata = db_instance.Column(db_instance.Text)  # Renamed from 'metadata' (reserved)
        timestamp = db_instance.Column(db_instance.DateTime, default=datetime.utcnow, nullable=False)
        ip_address = db_instance.Column(db_instance.String(45))
        user_agent = db_instance.Column(db_instance.String(500))
        
        def __repr__(self):
            return f'<AnalyticsEvent {self.event_type}:{self.event_name}>'
    
    class AIUsageLog(db_instance.Model):
        """Track AI feature usage"""
        __tablename__ = 'ai_usage_logs'
        
        id = db_instance.Column(db_instance.Integer, primary_key=True)
        user_id = db_instance.Column(db_instance.Integer, db_instance.ForeignKey('user.id'), nullable=True)
        feature_name = db_instance.Column(db_instance.String(100), nullable=False)
        api_call_count = db_instance.Column(db_instance.Integer, default=1)
        tokens_used = db_instance.Column(db_instance.Integer, default=0)
        cost_estimate = db_instance.Column(db_instance.Float, default=0.0)
        success = db_instance.Column(db_instance.Boolean, default=True)
        error_message = db_instance.Column(db_instance.Text, nullable=True)
        usage_metadata = db_instance.Column(db_instance.Text)  # Renamed from 'metadata' (reserved)
        timestamp = db_instance.Column(db_instance.DateTime, default=datetime.utcnow, nullable=False)
        
        def __repr__(self):
            return f'<AIUsageLog {self.feature_name}:{self.user_id}>'
    
    return AnalyticsEvent, AIUsageLog

# Initialize models when db is available
AnalyticsEvent = None
AIUsageLog = None

def track_event(event_type, event_name, user_id=None, metadata=None, request=None):
    """Track an analytics event"""
    try:
        event = AnalyticsEvent(
            user_id=user_id,
            event_type=event_type,
            event_name=event_name,
            event_metadata=json.dumps(metadata) if metadata else None,
            ip_address=request.remote_addr if request else None,
            user_agent=request.headers.get('User-Agent') if request else None
        )
        db.session.add(event)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(f"Error tracking event: {e}")
        return False

def track_ai_usage(feature_name, user_id=None, tokens_used=0, success=True, 
                  error_message=None, metadata=None):
    """Track AI feature usage"""
    if not db or AIUsageLog is None:
        return False
    try:
        # Estimate cost (rough estimates based on GPT-4o-mini pricing)
        cost_per_1k_tokens = 0.00015  # $0.15 per 1M tokens
        cost_estimate = (tokens_used / 1000) * cost_per_1k_tokens
        
        log = AIUsageLog(
            user_id=user_id,
            feature_name=feature_name,
            tokens_used=tokens_used,
            cost_estimate=cost_estimate,
            success=success,
            error_message=error_message,
            usage_metadata=json.dumps(metadata) if metadata else None
        )
        db.session.add(log)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(f"Error tracking AI usage: {e}")
        return False

def get_analytics_summary(days=30):
    """Get analytics summary for the last N days"""
    if not db or AnalyticsEvent is None or AIUsageLog is None:
        return {
            'page_views': 0,
            'ai_usage': [],
            'claims_filed': 0,
            'documents_uploaded': 0,
            'period_days': days
        }
    
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    
    try:
        # Page views
        page_views = AnalyticsEvent.query.filter(
            AnalyticsEvent.event_type == 'page_view',
            AnalyticsEvent.timestamp >= cutoff_date
        ).count()
        
        # AI feature usage
        ai_usage = db.session.query(
            AIUsageLog.feature_name,
            func.count(AIUsageLog.id).label('count'),
            func.sum(AIUsageLog.tokens_used).label('total_tokens'),
            func.sum(AIUsageLog.cost_estimate).label('total_cost')
        ).filter(
            AIUsageLog.timestamp >= cutoff_date
        ).group_by(AIUsageLog.feature_name).all()
        
        # Claims filed
        claims_filed = AnalyticsEvent.query.filter(
            AnalyticsEvent.event_type == 'claim_filed',
            AnalyticsEvent.timestamp >= cutoff_date
        ).count()
        
        # Documents uploaded
        documents_uploaded = AnalyticsEvent.query.filter(
            AnalyticsEvent.event_type == 'document_uploaded',
            AnalyticsEvent.timestamp >= cutoff_date
        ).count()
        
        return {
            'page_views': page_views,
            'ai_usage': [
                {
                    'feature': usage.feature_name,
                    'count': usage.count,
                    'tokens': usage.total_tokens or 0,
                    'cost': float(usage.total_cost or 0)
                }
                for usage in ai_usage
            ],
            'claims_filed': claims_filed,
            'documents_uploaded': documents_uploaded,
            'period_days': days
        }
    except Exception as e:
        print(f"Error getting analytics summary: {e}")
        return {
            'page_views': 0,
            'ai_usage': [],
            'claims_filed': 0,
            'documents_uploaded': 0,
            'period_days': days
        }

def get_ai_usage_stats(days=30):
    """Get detailed AI usage statistics"""
    if not db or AIUsageLog is None:
        return {
            'total_calls': 0,
            'total_tokens': 0,
            'total_cost': 0.0,
            'avg_cost': 0.0,
            'success_rate': 0.0,
            'period_days': days
        }
    
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    
    try:
        stats = db.session.query(
            func.count(AIUsageLog.id).label('total_calls'),
            func.sum(AIUsageLog.tokens_used).label('total_tokens'),
            func.sum(AIUsageLog.cost_estimate).label('total_cost'),
            func.avg(AIUsageLog.cost_estimate).label('avg_cost'),
            func.sum(func.cast(AIUsageLog.success, db.Integer)).label('success_count')
        ).filter(
            AIUsageLog.timestamp >= cutoff_date
        ).first()
        
        return {
            'total_calls': stats.total_calls or 0,
            'total_tokens': stats.total_tokens or 0,
            'total_cost': float(stats.total_cost or 0),
            'avg_cost': float(stats.avg_cost or 0),
            'success_rate': (stats.success_count or 0) / (stats.total_calls or 1) * 100 if stats.total_calls else 0,
            'period_days': days
        }
    except Exception as e:
        print(f"Error getting AI usage stats: {e}")
        return {
            'total_calls': 0,
            'total_tokens': 0,
            'total_cost': 0.0,
            'avg_cost': 0.0,
            'success_rate': 0.0,
            'period_days': days
        }

