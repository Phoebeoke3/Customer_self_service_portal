# SwissAxa Customer Self-Service Portal - UML Architecture Diagrams

This document contains the "To Be" architecture diagrams for the SwissAxa Customer Self-Service Portal project.

## Diagram Files

- **UML_DIAGRAM.puml** - PlantUML source file containing all diagrams

## Diagrams Included

### 1. System Architecture / Component Diagram
Shows the overall system architecture with:
- Client Layer (Web Browser, Mobile App)
- Presentation Layer (Flask Web Application, REST API)
- Business Logic Layer (AI Services, Email, Notifications, Bank API, Analytics)
- Data Layer (SQLite Database, File Storage)
- External Services (OpenAI, SMTP, Google Maps, Bank APIs)

### 2. Database Models (Class Diagram)
Complete entity-relationship diagram showing:
- All database models (User, Agent, Policies, Claims, Documents, etc.)
- Relationships between entities
- Primary keys, foreign keys, and attributes

### 3. Use Case Diagram
Comprehensive use cases for:
- Customer actions (policies, claims, documents, bank, services)
- Agent interactions
- Admin functions
- AI-powered features

### 4. Sequence Diagram: AI-Powered Claim Filing
Detailed flow showing:
- Customer filing a claim with photos/videos
- AI analysis using OpenAI Vision API
- Database storage
- Notification and email sending

### 5. Deployment Diagram
Infrastructure deployment showing:
- Client devices
- Web server (Nginx, WSGI, Flask)
- Application server (Database, File Storage, Cache)
- External service integrations

### 6. Service Architecture Diagram
Microservices-style architecture showing:
- Frontend services
- API Gateway
- Core services
- AI services orchestration
- Integration services
- Data services

## How to View the Diagrams

### Option 1: Online PlantUML Viewer (Recommended)
1. Go to [PlantUML Online Server](http://www.plantuml.com/plantuml/uml/)
2. Copy the content from `UML_DIAGRAM.puml`
3. Paste it into the online editor
4. The diagrams will be rendered automatically

### Option 2: VS Code Extension
1. Install the "PlantUML" extension in VS Code
2. Open `UML_DIAGRAM.puml`
3. Press `Alt+D` (or right-click → Preview) to view diagrams

### Option 3: Command Line (PlantUML Java)
1. Install PlantUML: `npm install -g node-plantuml` or download from [PlantUML website](https://plantuml.com/download)
2. Generate images:
   ```bash
   plantuml UML_DIAGRAM.puml
   ```
3. This will create PNG/SVG files for each diagram

### Option 4: Split into Separate Files
If you want to view individual diagrams, you can split the file:
- Each `@startuml` block is a separate diagram
- Each `@enduml` marks the end of a diagram

## Architecture Overview

### Key Components

1. **Client Layer**
   - Web browsers accessing the portal
   - Mobile applications using REST API

2. **Presentation Layer**
   - Flask web application with modular routes
   - REST API for mobile integration
   - Authentication and authorization

3. **Business Logic Layer**
   - AI Services: Policy comparison, document tagging, claims analysis, chatbot
   - Email Service: SMTP integration for notifications
   - Notification Service: In-app notifications
   - Bank API Integration: Sparkasse, N26, Deutsche Bank
   - Analytics Service: Usage tracking and reporting
   - i18n Service: Multi-language support (German/English)

4. **Data Layer**
   - SQLite database with 12+ models
   - File storage for documents, policies, and claim media

5. **External Services**
   - OpenAI API (GPT-4o-mini, GPT-4o Vision)
   - SMTP servers for email
   - Google Maps API for geolocation
   - Bank APIs for financial transactions

### Key Features

- **AI-Powered Services**: 8 different AI features integrated
- **Multi-Channel Access**: Web and mobile API support
- **Comprehensive Testing**: 76 unit tests with 77% coverage
- **Scalable Architecture**: Modular design for easy extension
- **Security**: Authentication, password hashing, file validation
- **Internationalization**: German and English support

## Technology Stack

- **Backend**: Flask (Python 3.12)
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **AI**: OpenAI API (GPT-4o-mini, GPT-4o Vision)
- **Email**: Flask-Mail (SMTP)
- **Testing**: pytest, pytest-cov
- **API**: RESTful API for mobile apps

## Future Enhancements

The architecture supports:
- Migration to PostgreSQL/MySQL for production
- Microservices architecture
- Docker containerization
- Kubernetes orchestration
- Real-time notifications (WebSockets)
- Advanced caching (Redis)
- Load balancing
- API rate limiting
- OAuth2 authentication

## Notes

- The diagrams represent the "To Be" state - the intended architecture
- Current implementation uses SQLite (can be upgraded to PostgreSQL)
- AI services have fallback mechanisms when API key is not configured
- All external integrations are optional and have mock implementations

