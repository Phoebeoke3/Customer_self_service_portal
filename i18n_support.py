"""
Internationalization (i18n) Support for SwissAxa Portal
Supports German and English languages
"""
from flask import request, session
from flask_babel import Babel, gettext as _, lazy_gettext as _l
import os

babel = Babel()

# Language mappings
SUPPORTED_LANGUAGES = {
    'en': 'English',
    'de': 'Deutsch'
}

def init_i18n(app):
    """Initialize i18n with Flask app"""
    app.config['LANGUAGES'] = SUPPORTED_LANGUAGES
    app.config['BABEL_DEFAULT_LOCALE'] = os.getenv('DEFAULT_LANGUAGE', 'en')
    app.config['BABEL_DEFAULT_TIMEZONE'] = 'UTC'
    
    babel.init_app(app)
    return babel

@babel.localeselector
def get_locale():
    """Determine the best matching language"""
    # Check session first
    if 'language' in session:
        return session.get('language')
    
    # Check request header
    return request.accept_languages.best_match(SUPPORTED_LANGUAGES.keys()) or 'en'

def set_language(language_code):
    """Set language for current session"""
    if language_code in SUPPORTED_LANGUAGES:
        session['language'] = language_code
        return True
    return False

# Translation helper functions
def translate(text, language=None):
    """Translate text to specified language"""
    if language and language in SUPPORTED_LANGUAGES:
        # In a real implementation, you would use gettext with proper .po files
        # For now, return a simple mapping
        translations = {
            'en': {
                'Dashboard': 'Dashboard',
                'myPolicies': 'myPolicies',
                'myDocuments': 'myDocuments',
                'myBank': 'myBank',
                'myServices': 'myServices',
                'myInformation': 'myInformation',
            },
            'de': {
                'Dashboard': 'Dashboard',
                'myPolicies': 'Meine Policen',
                'myDocuments': 'Meine Dokumente',
                'myBank': 'Meine Bank',
                'myServices': 'Meine Services',
                'myInformation': 'Meine Informationen',
            }
        }
        return translations.get(language, {}).get(text, text)
    return text

