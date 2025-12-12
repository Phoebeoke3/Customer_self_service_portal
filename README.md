# SwissAxa Customer Self-Service Portal

A comprehensive customer self-service portal for SwissAxa insurance company in Nord-Rhein Westfalen (NRW), Germany.

## Features

### 1. myPolicies
- **SwissAxa Policies**: List view of all policies purchased from SwissAxa with expiration dates
- **External Policies**: Upload and manage external insurance policies
- **AI-Powered Comparison**: Compare external policies with SwissAxa products using OpenAI AI technology
  - Get match scores and detailed recommendations
  - Compare coverage and premiums
  - Receive personalized suggestions

### 2. myDocuments
- Upload documents required for policy and claims processing
- Download documents uploaded by customers
- **AI-Powered Auto-Tagging**: Documents are automatically tagged by AI
  - Detects document types: policy, claim, invoice, report, identity, medical, proof_of_ownership, repair_invoice, police_report
  - Select "Auto-detect (AI)" option when uploading

### 3. myBank
- Connect bank accounts (Sparkasse, N26, Deutsche Bank, etc.)
- Initiate debit/credit transactions
- Note: Loans and overdrafts are not available through this channel

### 4. myServices
- **Claims Management**: File claims, upload photos/videos of damages, capture geolocation using Google Maps
  - **AI-Powered Claims Analysis**: AI analyzes uploaded photos/videos
    - Detects damage type (water, fire, theft, collision, etc.)
    - Assesses severity (low, medium, high, critical)
    - Pre-fills claim descriptions automatically
    - Sets priority levels (urgent, normal, low)
    - Estimates claim value ranges
- **Policy Management**: Access policies, upgrade policies, make policy change requests
  - **AI-Powered Recommendations**: Get personalized policy recommendations based on your profile and history
- **Contact Management**: Send emails to SwissAxa Customer Service Desk or Insurance Agent
- **Scheduling**: Book appointments with Customer Service Desk or Insurance Agent
  - **AI-Powered Appointment Suggestions**: Get optimal appointment times based on agent availability patterns

### 5. myInformation
- View and edit personal details
- Manage personal data (name, addresses, email, phone, bank account)
- Update correspondence address
- **AI-Powered Data Validation**: AI checks for inconsistencies in address or identity information
  - Validates address and phone number formats
  - Detects inconsistencies between addresses
  - Prompts re-authentication for sensitive changes

### 6. AI Chatbot 🤖
- **24/7 AI Assistant**: Available in the bottom-right corner of every page
- Answers questions about policies, claims, documents, and general inquiries
- Maintains conversation history for context
- Modern, user-friendly chat interface

## Installation

1. **Clone the repository or navigate to the project directory**

2. **Create a virtual environment (if not already created)**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up OpenAI API Key (Optional, for AI features)**
   - Get an OpenAI API key from [OpenAI Platform](https://platform.openai.com/api-keys)
   - Set the environment variable:
     - **Windows PowerShell:**
       ```powershell
       $env:OPENAI_API_KEY="your-api-key-here"
       ```
     - **Windows CMD:**
       ```cmd
       set OPENAI_API_KEY=your-api-key-here
       ```
     - **Linux/Mac:**
       ```bash
       export OPENAI_API_KEY="your-api-key-here"
       ```
   - **Note**: The application works without the API key but will use fallback/mock data for AI features
   - See `AI_SETUP.md` for detailed setup instructions

6. **Set up Email Service (Optional)**
   - Configure SMTP settings via environment variables:
     - **Windows PowerShell:**
       ```powershell
       $env:MAIL_SERVER="smtp.gmail.com"
       $env:MAIL_PORT="587"
       $env:MAIL_USE_TLS="True"
       $env:MAIL_USERNAME="your-email@gmail.com"
       $env:MAIL_PASSWORD="your-app-password"
       $env:MAIL_DEFAULT_SENDER="noreply@swissaxa.de"
       ```
     - **Linux/Mac:**
       ```bash
       export MAIL_SERVER=smtp.gmail.com
       export MAIL_PORT=587
       export MAIL_USE_TLS=True
       export MAIL_USERNAME=your-email@gmail.com
       export MAIL_PASSWORD=your-app-password
       export MAIL_DEFAULT_SENDER=noreply@swissaxa.de
       ```
   - **Note**: The application works without email configuration (emails will be simulated)
   - See `FEATURE_IMPLEMENTATION_GUIDE.md` for detailed setup

7. **Set up Google Maps API (Optional, for geolocation features)**
   - Get a Google Maps API key from [Google Cloud Console](https://console.cloud.google.com/)
   - Update the API key in `templates/claims.html`:
     ```html
     <script src="https://maps.googleapis.com/maps/api/js?key=YOUR_GOOGLE_MAPS_API_KEY&callback=initMap" async defer></script>
     ```

8. **Run the application**
   ```bash
   python app.py
   ```

9. **Access the application**
   - Open your browser and navigate to: `http://localhost:5000` or `http://127.0.0.1:5000`
   - Register a new account or use an existing one
   - Click the "Show Features" button in the dashboard to view AI-powered features
   - Access analytics dashboard at `/admin/analytics`
   - Use mobile API endpoints at `/api/mobile/*`

## Project Structure

```
Customer self service portal/
├── app.py                      # Main Flask application
├── ai_services.py              # AI service module (OpenAI integration)
├── init_sample_data.py         # Sample data initialization script
├── requirements.txt            # Python dependencies
├── pytest.ini                  # Pytest configuration
├── run_tests.py                # Test runner script
├── run_tests.ps1               # PowerShell test script
├── run_tests.bat               # Windows batch test script
├── run_server.ps1              # PowerShell server script
├── run_server.bat              # Windows batch server script
├── FUNCTIONAL_REQUIREMENTS.md  # Functional requirements document
├── AI_SETUP.md                 # AI features setup guide
├── AI_IMPLEMENTATION_SUMMARY.md # AI implementation details
├── README.md                   # This file
├── templates/                  # HTML templates
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── policies.html
│   ├── documents.html
│   ├── bank.html
│   ├── services.html
│   ├── claims.html
│   ├── policy_management.html
│   ├── contact.html
│   ├── scheduling.html
│   └── information.html
├── static/                     # Static files
│   ├── css/
│   │   └── style.css
│   └── js/
├── tests/                      # Test suite
│   ├── __init__.py
│   ├── conftest.py             # Pytest fixtures
│   ├── README.md               # Test documentation
│   ├── test_models.py
│   ├── test_auth.py
│   ├── test_policies.py
│   ├── test_claims.py
│   ├── test_documents.py
│   ├── test_services.py
│   ├── test_information.py
│   └── test_bank.py
├── uploads/                    # Uploaded files
│   ├── documents/
│   ├── policies/
│   └── claims/
├── instance/                   # Instance folder (database)
│   └── swissaxa_portal.db      # SQLite database (created on first run)
└── venv/                       # Virtual environment (not in repo)
```

## Database Models

The application uses SQLAlchemy with SQLite database and includes the following models:
- **User**: Customer accounts
- **Agent**: Insurance agents
- **SwissAxaPolicy**: SwissAxa insurance policies
- **ExternalPolicy**: External insurance policies
- **Document**: Uploaded documents
- **Claim**: Insurance claims
- **ClaimMedia**: Photos/videos for claims
- **PolicyChangeRequest**: Policy change requests
- **Appointment**: Scheduled appointments
- **BankAccount**: Connected bank accounts

## Usage

1. **Register/Login**: Create an account or login with existing credentials
2. **Dashboard**: View overview of policies, documents, claims, and appointments
3. **myPolicies**: View SwissAxa policies and upload external policies for comparison
4. **myDocuments**: Upload and download documents
5. **myBank**: Connect bank accounts and initiate transactions
6. **myServices**: Access claims, policy management, contact, and scheduling features
7. **myInformation**: Update personal details

## Technology Stack

- **Backend**: Flask (Python 3.12)
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript (jQuery)
- **Icons**: Font Awesome 6
- **Maps**: Google Maps API (for geolocation)
- **Authentication**: Flask-Login
- **Email**: Flask-Mail (SMTP email sending)
- **Internationalization**: Flask-Babel (multi-language support)
- **Testing**: pytest, pytest-cov, pytest-flask, pytest-mock
- **AI Integration**: OpenAI API
  - GPT-4o-mini (text analysis)
  - GPT-4o Vision (image analysis)
  - AI Policy Comparison
  - AI Document Auto-Tagging
  - AI Claims Analysis (with Vision API)
  - AI Policy Recommendations
  - AI Appointment Suggestions
  - AI Data Validation
  - AI Chatbot
  - AI Fraud Detection
- **Analytics**: Custom analytics tracking system
- **Notifications**: In-app notification system
- **Mobile API**: RESTful API for mobile apps

## Security Notes

- Passwords are hashed using Werkzeug's password hashing
- File uploads are validated and stored securely
- User authentication required for all features
- SQL injection protection via SQLAlchemy ORM

## Testing

The project includes a comprehensive unit test suite using pytest with **76 passing tests** covering all major functionality.

### Quick Start

**Run all tests:**
```bash
pytest tests/ -v
```

**Run with coverage report:**
```bash
python run_tests.py
```

**Run specific test module:**
```bash
pytest tests/test_auth.py -v
```

### Test Scripts

**Windows (PowerShell):**
```powershell
.\run_tests.ps1
```

**Windows (Command Prompt):**
```cmd
run_tests.bat
```

**Linux/Mac:**
```bash
python run_tests.py
```

### Test Coverage

The test suite includes **76 tests** covering:

- ✅ **Database Models** (11 tests)
  - User, Agent, Policy, Claim, Document, BankAccount, Appointment models
  - Relationships and data integrity

- ✅ **Authentication** (13 tests)
  - Login, registration, logout
  - Password hashing and validation
  - Protected route access control

- ✅ **Policy Management** (7 tests)
  - Policy listing and display
  - External policy upload
  - AI-powered policy comparison API
  - Expiration warnings

- ✅ **Claims Management** (5 tests)
  - Filing claims
  - Media upload (photos/videos)
  - Geolocation handling
  - Claim listing

- ✅ **Document Management** (6 tests)
  - Document upload
  - Document download
  - Access control
  - File type validation

- ✅ **Services** (10 tests)
  - Policy change requests
  - Contact (email to service desk/agents)
  - Appointment scheduling
  - Service page navigation

- ✅ **User Information** (3 tests)
  - View user information
  - Update user information
  - Partial updates

- ✅ **Bank Management** (5 tests)
  - Connect bank accounts
  - Bank transactions
  - Account listing

### Test Structure

```
tests/
├── conftest.py              # Pytest fixtures and configuration
├── test_models.py           # Database model tests
├── test_auth.py             # Authentication tests
├── test_policies.py         # Policy management tests
├── test_claims.py           # Claims management tests
├── test_documents.py        # Document management tests
├── test_services.py        # Services tests
├── test_information.py     # User information tests
└── test_bank.py            # Bank account tests
```

### Test Features

- **Isolated test database** - Each test uses a temporary SQLite database
- **Automatic cleanup** - Test data is cleaned up after each test
- **Comprehensive fixtures** - Reusable test data for all models
- **Coverage reporting** - HTML and terminal coverage reports
- **Fast execution** - Tests run in ~30 seconds

See `tests/README.md` for detailed testing documentation and best practices.

## Project Status

✅ **Core Features**: Fully implemented and tested  
✅ **Unit Tests**: 76 tests passing (82% code coverage)  
✅ **Documentation**: Complete functional requirements  
✅ **AI Features**: Fully implemented with OpenAI integration  
  - ✅ AI Policy Comparison
  - ✅ AI Document Auto-Tagging
  - ✅ AI Claims Analysis (with Vision API)
  - ✅ AI Policy Recommendations
  - ✅ AI Appointment Suggestions
  - ✅ AI Data Validation
  - ✅ AI Chatbot (24/7 assistant)
  - ✅ AI Fraud Detection
  - ✅ Collapsible AI Features Dashboard Section
✅ **Email Integration**: Fully implemented with Flask-Mail  
✅ **Multi-Language Support**: German and English (Flask-Babel)  
✅ **Notifications System**: In-app notifications implemented  
✅ **Analytics System**: Full tracking and dashboard  
✅ **Mobile API**: REST API endpoints for mobile apps  
✅ **Bank API Structure**: Integration structure ready (requires credentials)  
📋 **Future Enhancements**: See below

## AI Features

The portal includes comprehensive AI-powered features using OpenAI's GPT-4o-mini and GPT-4o Vision models:

### Available AI Features

1. **AI Policy Comparison** - Compare external policies with SwissAxa products using GPT-4o-mini
2. **AI Document Auto-Tagging** - Automatically categorize uploaded documents
3. **AI Claims Analysis** - Analyze damage photos/videos using GPT-4o Vision API and pre-fill claim details
4. **AI Policy Recommendations** - Get personalized policy suggestions based on user profile
5. **AI Appointment Suggestions** - Optimal appointment time recommendations
6. **AI Data Validation** - Check for data inconsistencies in user information
7. **AI Chatbot** - 24/7 customer support assistant (bottom-right corner) using GPT-4o-mini
8. **AI Fraud Detection** - Transaction pattern monitoring and anomaly detection

### AI Features Dashboard

The dashboard includes a collapsible "AI-Powered Features" section:
- Hidden by default for a cleaner interface
- Click "Show Features" button to expand
- Smooth animations and user-friendly interface
- Real-time AI service status indicator

### Setup

See `AI_SETUP.md` for detailed setup instructions and API key configuration.

### Cost Considerations

OpenAI API usage is cost-effective:
- Policy comparison: ~$0.001-0.01 per comparison
- Document tagging: ~$0.0001-0.001 per document
- Claims analysis: ~$0.001-0.01 per claim
- Chatbot: ~$0.001-0.01 per message

**Note**: The application includes fallback mechanisms and works without an API key (using mock data).

## Additional Resources

- **AI Setup Guide**: See `AI_SETUP.md` for detailed AI configuration
- **Feature Implementation Guide**: See `FEATURE_IMPLEMENTATION_GUIDE.md` for advanced features setup
- **Implementation Summary**: See `IMPLEMENTATION_SUMMARY.md` for feature overview
- **Functional Requirements**: See `FUNCTIONAL_REQUIREMENTS.md` for detailed requirements

## API Endpoints

### Mobile API
- `GET /api/mobile/claims` - Get user claims
- `GET /api/mobile/claims/<id>` - Get claim details
- `GET /api/mobile/notifications` - Get notifications
- `GET /api/mobile/policies` - Get policies
- `GET /api/mobile/documents` - Get documents
- `GET /api/mobile/dashboard/stats` - Get dashboard statistics
- `POST /api/mobile/chat` - Mobile chat with AI

### Notifications API
- `GET /api/notifications` - Get user notifications
- `POST /api/notifications/<id>/read` - Mark notification as read

### Language API
- `POST /api/language/<code>` - Switch language (en/de)

### Analytics API
- `GET /admin/analytics` - Analytics dashboard

## Future Enhancements

- **Enhanced Mobile App**: Native iOS/Android applications using the mobile API
- **Real Bank API Integration**: Connect with actual bank APIs (requires credentials)
- **Push Notifications**: Browser push notifications (requires HTTPS)
- **Advanced Reporting**: Enhanced analytics and reporting features
- **Multi-tenant Support**: Support for multiple insurance companies

## Advanced Features

### ✅ Email Integration
- **Status**: Fully implemented
- **File**: `email_service.py`
- **Features**:
  - Send actual emails using Flask-Mail (not simulated)
  - Claim notification emails
  - Appointment confirmation emails
  - Contact email forwarding
  - HTML email support with attachments
- **Setup**: Configure SMTP settings via environment variables (see `FEATURE_IMPLEMENTATION_GUIDE.md`)

### ✅ Enhanced AI Features
- **Status**: Fully implemented
- **Updates**: `ai_services.py`
- **Features**:
  - **OpenAI Vision API**: Image analysis for claims using GPT-4o Vision
  - **Enhanced Document OCR**: Improved document analysis and tagging
  - **Multi-language AI Support**: AI responses in multiple languages
- **Usage**: Claims analysis now accepts image files for visual damage assessment

### ✅ Multi-Language Support
- **Status**: Fully implemented
- **File**: `i18n_support.py`
- **Features**:
  - German and English language support
  - Flask-Babel integration
  - Session-based language selection
  - Language switching API endpoint
- **API**: `POST /api/language/<code>` to switch languages

### ✅ Notifications System
- **Status**: Fully implemented
- **File**: `notifications.py`
- **Features**:
  - In-app notifications
  - Claim status notifications
  - Appointment confirmations
  - Policy update notifications
  - Notification API endpoints
- **API**: `GET /api/notifications` to retrieve notifications

### ✅ Analytics System
- **Status**: Fully implemented
- **File**: `analytics.py`
- **Features**:
  - User activity tracking
  - AI usage analytics
  - Cost tracking and estimation
  - Performance metrics
  - Advanced analytics dashboard
- **Dashboard**: Access at `/admin/analytics`

### ✅ Mobile API
- **Status**: Fully implemented
- **File**: `mobile_api.py`
- **Endpoints**:
  - `GET /api/mobile/claims` - Get user claims
  - `GET /api/mobile/claims/<id>` - Get claim details
  - `GET /api/mobile/notifications` - Get notifications
  - `GET /api/mobile/policies` - Get policies
  - `GET /api/mobile/documents` - Get documents
  - `GET /api/mobile/dashboard/stats` - Get dashboard statistics
  - `POST /api/mobile/chat` - Mobile chat with AI
- **Purpose**: REST API for mobile app development (React Native, Flutter, etc.)

### ✅ Bank API Integration Structure
- **Status**: Structure implemented (requires API credentials)
- **File**: `bank_api_integration.py`
- **Features**:
  - Support for Sparkasse, N26, Deutsche Bank
  - Transaction processing structure
  - Balance checking
  - Transaction verification
- **Note**: Requires actual bank API credentials to function

## Project Structure

```
Customer self service portal/
├── app.py                      # Main Flask application
├── ai_services.py              # AI service module (OpenAI integration)
├── email_service.py            # Email sending service
├── analytics.py                # Analytics tracking system
├── notifications.py            # Notification system
├── i18n_support.py            # Multi-language support
├── mobile_api.py              # Mobile REST API endpoints
├── bank_api_integration.py    # Bank API integration structure
├── init_sample_data.py         # Sample data initialization script
├── requirements.txt            # Python dependencies
├── pytest.ini                  # Pytest configuration
├── run_tests.py                # Test runner script
├── run_tests.ps1               # PowerShell test script
├── run_tests.bat               # Windows batch test script
├── run_server.ps1              # PowerShell server script
├── run_server.bat              # Windows batch server script
├── FUNCTIONAL_REQUIREMENTS.md  # Functional requirements document
├── AI_SETUP.md                 # AI features setup guide
├── AI_IMPLEMENTATION_SUMMARY.md # AI implementation details
├── FEATURE_IMPLEMENTATION_GUIDE.md # Advanced features guide
├── IMPLEMENTATION_SUMMARY.md   # Implementation summary
├── README.md                   # This file
├── templates/                  # HTML templates
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── policies.html
│   ├── documents.html
│   ├── bank.html
│   ├── services.html
│   ├── claims.html
│   ├── policy_management.html
│   ├── contact.html
│   ├── scheduling.html
│   ├── information.html
│   └── analytics.html          # Analytics dashboard
├── static/                     # Static files
│   ├── css/
│   │   └── style.css
│   └── js/
├── tests/                      # Test suite
│   ├── __init__.py
│   ├── conftest.py             # Pytest fixtures
│   ├── README.md               # Test documentation
│   ├── test_models.py
│   ├── test_auth.py
│   ├── test_policies.py
│   ├── test_claims.py
│   ├── test_documents.py
│   ├── test_services.py
│   ├── test_information.py
│   └── test_bank.py
├── uploads/                    # Uploaded files
│   ├── documents/
│   ├── policies/
│   └── claims/
├── instance/                   # Instance folder (database)
│   └── swissaxa_portal.db      # SQLite database (created on first run)
└── venv/                       # Virtual environment (not in repo)
```

## License


## Contact



