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

6. **Set up Google Maps API (Optional, for geolocation features)**
   - Get a Google Maps API key from [Google Cloud Console](https://console.cloud.google.com/)
   - Update the API key in `templates/claims.html`:
     ```html
     <script src="https://maps.googleapis.com/maps/api/js?key=YOUR_GOOGLE_MAPS_API_KEY&callback=initMap" async defer></script>
     ```

7. **Run the application**
   ```bash
   python app.py
   ```

8. **Access the application**
   - Open your browser and navigate to: `http://localhost:5000` or `http://127.0.0.1:5000`
   - Register a new account or use an existing one
   - Click the "Show Features" button in the dashboard to view AI-powered features

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
- **Testing**: pytest, pytest-cov, pytest-flask, pytest-mock
- **AI Integration**: OpenAI API (GPT-4o-mini)
  - AI Policy Comparison
  - AI Document Auto-Tagging
  - AI Claims Analysis
  - AI Policy Recommendations
  - AI Appointment Suggestions
  - AI Data Validation
  - AI Chatbot
  - AI Fraud Detection

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
  - ✅ AI Claims Analysis
  - ✅ AI Policy Recommendations
  - ✅ AI Appointment Suggestions
  - ✅ AI Data Validation
  - ✅ AI Chatbot (24/7 assistant)
  - ✅ AI Fraud Detection
  - ✅ Collapsible AI Features Dashboard Section
📋 **Future Enhancements**: See below

## AI Features

The portal includes comprehensive AI-powered features using OpenAI's GPT-4o-mini model:

### Available AI Features

1. **AI Policy Comparison** - Compare external policies with SwissAxa products
2. **AI Document Auto-Tagging** - Automatically categorize uploaded documents
3. **AI Claims Analysis** - Analyze damage photos/videos and pre-fill claim details
4. **AI Policy Recommendations** - Get personalized policy suggestions
5. **AI Appointment Suggestions** - Optimal appointment time recommendations
6. **AI Data Validation** - Check for data inconsistencies
7. **AI Chatbot** - 24/7 customer support assistant (bottom-right corner)
8. **AI Fraud Detection** - Transaction pattern monitoring

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

## Future Enhancements

- **Email Integration**: Send actual emails (currently simulated)
- **Bank API Integration**: Real transaction processing with bank APIs
- **Advanced AI Features**: 
  - Image analysis for claims using OpenAI Vision API
  - Enhanced document OCR and analysis
  - Multi-language AI support
- **Notifications**: Push notifications for claims and appointment updates
- **Mobile App**: Native mobile application version
- **Multi-language**: Full German and English support
- **Advanced Analytics**: Dashboard with insights and reporting
- **AI Usage Analytics**: Monitor and optimize AI feature usage

## License


## Contact



