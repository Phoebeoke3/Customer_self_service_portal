# SwissAxa Customer Self-Service Portal

A comprehensive customer self-service portal for SwissAxa insurance company in Nord-Rhein Westfalen (NRW), Germany.

## Features

### 1. myPolicies
- **SwissAxa Policies**: List view of all policies purchased from SwissAxa with expiration dates
- **External Policies**: Upload and manage external insurance policies
- **AI-Powered Comparison**: Compare external policies with SwissAxa products using AI technology

### 2. myDocuments
- Upload documents required for policy and claims processing
- Download documents uploaded by customers
- Organize documents by type (policy, claim, identity, medical, etc.)

### 3. myBank
- Connect bank accounts (Sparkasse, N26, Deutsche Bank, etc.)
- Initiate debit/credit transactions
- Note: Loans and overdrafts are not available through this channel

### 4. myServices
- **Claims Management**: File claims, upload photos/videos of damages, capture geolocation using Google Maps
- **Policy Management**: Access policies, upgrade policies, make policy change requests
- **Contact Management**: Send emails to SwissAxa Customer Service Desk or Insurance Agent
- **Scheduling**: Book appointments with Customer Service Desk or Insurance Agent

### 5. myInformation
- View and edit personal details
- Manage personal data (name, addresses, email, phone, bank account)
- Update correspondence address

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

5. **Set up Google Maps API (Optional, for geolocation features)**
   - Get a Google Maps API key from [Google Cloud Console](https://console.cloud.google.com/)
   - Update the API key in `templates/claims.html`:
     ```html
     <script src="https://maps.googleapis.com/maps/api/js?key=YOUR_GOOGLE_MAPS_API_KEY&callback=initMap" async defer></script>
     ```

6. **Run the application**
   ```bash
   python app.py
   ```

7. **Access the application**
   - Open your browser and navigate to: `http://localhost:5000`
   - Register a new account or use an existing one

## Project Structure

```
Customer service self portal/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── templates/            # HTML templates
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
├── static/               # Static files
│   ├── css/
│   │   └── style.css
│   └── js/
├── uploads/             # Uploaded files
│   ├── documents/
│   ├── policies/
│   └── claims/
└── swissaxa_portal.db   # SQLite database (created on first run)
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

- **Backend**: Flask (Python)
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Icons**: Font Awesome 6
- **Maps**: Google Maps API (for geolocation)
- **Authentication**: Flask-Login

## Security Notes

- Passwords are hashed using Werkzeug's password hashing
- File uploads are validated and stored securely
- User authentication required for all features
- SQL injection protection via SQLAlchemy ORM

## Future Enhancements

- Email integration for sending actual emails
- Bank API integration for real transaction processing
- Advanced AI policy comparison using OpenAI or similar
- Push notifications for claims and appointment updates
- Mobile app version
- Multi-language support (German, English)

## License


## Contact



