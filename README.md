# HOA Management System API

A comprehensive FastAPI backend for managing Homeowners Association operations with Neon PostgreSQL database support.

## 🚀 Features

- **Property Management**: Manage properties, units, and residents
- **Financial Tracking**: Handle payments, financial accounts, and management fees
- **Maintenance Requests**: Track maintenance requests with priorities and status
- **Enhanced Maintenance**: Advanced maintenance requests with contractor assignment, work logs, and more
- **Violation Management**: Manage community violations and fines
- **Meeting Management**: Schedule and track board meetings
- **Document Management**: Store and manage HOA documents
- **Service Provider & Contractor Management**: Track contractors and service providers
- **User & Role Management**: Manage users, roles, and enhanced resident profiles

## 🏗️ Architecture

```
app/
├── database.py              # Database connection and session management
├── main.py                 # FastAPI application entry point
├── models.py               # SQLAlchemy models for all entities
├── schemas.py              # Pydantic schemas for request/response validation
└── routes/                 # API route modules
    ├── properties.py       # Property management endpoints
    ├── units.py            # Unit management endpoints
    ├── residents.py        # Resident management endpoints
    ├── residents_enhanced.py # Enhanced resident endpoints
    ├── users.py            # User management endpoints
    ├── payments.py         # Payment tracking endpoints
    ├── maintenance.py      # Basic maintenance request endpoints
    ├── maintenance_enhanced.py # Enhanced maintenance & work log endpoints
    ├── contractors.py      # Contractor management endpoints
    └── violations.py       # Violation management endpoints
```

## 📋 Database Schema

The system includes the following main entities:

### Core Entities
- **Properties**: HOA properties with details like name, address, total units
- **Units**: Individual units within properties with specifications
- **Residents**: People living in units (owners, tenants, board members)
- **Enhanced Residents**: Residents with user linkage, roles, vehicles, pets, emergency contacts
- **Users**: System users with roles and authentication fields
- **Payments**: Financial transactions and fee payments
- **Maintenance Requests**: Service requests with priorities and tracking
- **Enhanced Maintenance Requests**: Advanced requests with categories, contractors, scheduling, and more
- **Maintenance Work Logs**: Track work performed on maintenance requests
- **Violations**: Community rule violations and enforcement
- **Meetings**: Board and community meetings
- **Documents**: File storage and management
- **Service Providers & Contractors**: Contractors and service companies
- **Financial Accounts**: Operating, reserve, and special assessment accounts
- **Management Fees**: Fee structure and billing configuration

## 🛠️ Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd hoa-backend
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Create a `.env` file in the root directory:
```env
DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/hoa_db
```

### 5. Run the Application
```bash
uvicorn app.main:app --reload
```

The API will be available at: http://127.0.0.1:8000

## 📚 API Documentation

### Interactive Documentation
- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

### API Endpoints

#### Properties
- `POST /properties/` - Create a new property
- `GET /properties/` - List all properties (with filtering)
- `GET /properties/{id}` - Get specific property
- `PUT /properties/{id}` - Update property
- `DELETE /properties/{id}` - Delete property
- `GET /properties/{id}/stats` - Get property statistics

#### Units
- `POST /units/` - Create a new unit
- `GET /units/` - List all units (with filtering)
- `GET /units/{id}` - Get specific unit
- `PUT /units/{id}` - Update unit
- `DELETE /units/{id}` - Delete unit
- `GET /units/property/{property_id}` - Get units by property
- `GET /units/{id}/stats` - Get unit statistics

#### Residents (Basic)
- `POST /residents/` - Create a new resident
- `GET /residents/` - List all residents (with filtering)
- `GET /residents/{id}` - Get specific resident
- `PUT /residents/{id}` - Update resident
- `DELETE /residents/{id}` - Delete resident
- `GET /residents/unit/{unit_id}` - Get residents by unit
- `GET /residents/{id}/stats` - Get resident statistics

#### Enhanced Residents
- `POST /residents-enhanced/` - Create a new enhanced resident
- `GET /residents-enhanced/` - List all enhanced residents (with filtering)
- `GET /residents-enhanced/{id}` - Get specific enhanced resident
- `PUT /residents-enhanced/{id}` - Update enhanced resident
- `DELETE /residents-enhanced/{id}` - Delete enhanced resident
- `GET /residents-enhanced/unit/{unit_id}` - Get enhanced residents by unit
- `GET /residents-enhanced/property/{property_id}` - Get enhanced residents by property
- `GET /residents-enhanced/user/{user_id}` - Get enhanced residents by user
- `PUT /residents-enhanced/{id}/activate` - Activate resident
- `PUT /residents-enhanced/{id}/deactivate` - Deactivate resident
- `PUT /residents-enhanced/{id}/set-primary` - Set as primary resident
- `GET /residents-enhanced/{id}/vehicles` - Get resident vehicles
- `GET /residents-enhanced/{id}/pets` - Get resident pets
- `GET /residents-enhanced/{id}/emergency-contact` - Get emergency contact
- `GET /residents-enhanced/stats/summary` - Get enhanced resident summary statistics

#### Users
- `POST /users/` - Create a new user
- `GET /users/` - List all users (with filtering)
- `GET /users/{id}` - Get specific user
- `PUT /users/{id}` - Update user
- `DELETE /users/{id}` - Delete user
- `GET /users/email/{email}` - Get user by email
- `GET /users/role/{role}` - Get users by role
- `PUT /users/{id}/verify-email` - Verify user email
- `PUT /users/{id}/activate` - Activate user
- `PUT /users/{id}/deactivate` - Deactivate user
- `GET /users/stats/summary` - Get user summary statistics
- `GET /users/{id}/residents` - Get residents linked to user

#### Payments
- `POST /payments/` - Create a new payment
- `GET /payments/` - List all payments (with filtering)
- `GET /payments/{id}` - Get specific payment
- `PUT /payments/{id}` - Update payment
- `DELETE /payments/{id}` - Delete payment
- `GET /payments/resident/{resident_id}` - Get payments by resident
- `GET /payments/unit/{unit_id}` - Get payments by unit
- `GET /payments/stats/summary` - Get payment summary statistics

#### Maintenance Requests (Basic)
- `POST /maintenance/` - Create a new maintenance request
- `GET /maintenance/` - List all requests (with filtering)
- `GET /maintenance/{id}` - Get specific request
- `PUT /maintenance/{id}` - Update request
- `DELETE /maintenance/{id}` - Delete request
- `GET /maintenance/unit/{unit_id}` - Get requests by unit
- `GET /maintenance/resident/{resident_id}` - Get requests by resident
- `GET /maintenance/stats/summary` - Get maintenance summary statistics

#### Enhanced Maintenance Requests
- `POST /maintenance-enhanced/requests/` - Create a new enhanced maintenance request
- `GET /maintenance-enhanced/requests/` - List all enhanced requests (with filtering)
- `GET /maintenance-enhanced/requests/{id}` - Get specific enhanced request
- `PUT /maintenance-enhanced/requests/{id}` - Update enhanced request
- `DELETE /maintenance-enhanced/requests/{id}` - Delete enhanced request
- `GET /maintenance-enhanced/requests/{id}/work-logs` - Get work logs for a request
- `GET /maintenance-enhanced/stats/summary` - Get enhanced maintenance summary statistics

#### Maintenance Work Logs
- `POST /maintenance-enhanced/work-logs/` - Create a new work log
- `GET /maintenance-enhanced/work-logs/` - List all work logs (with filtering)
- `GET /maintenance-enhanced/work-logs/{id}` - Get specific work log
- `PUT /maintenance-enhanced/work-logs/{id}` - Update work log
- `DELETE /maintenance-enhanced/work-logs/{id}` - Delete work log
- `GET /maintenance-enhanced/work-logs/stats/summary` - Get work log summary statistics

#### Contractors
- `POST /contractors/` - Create a new contractor
- `GET /contractors/` - List all contractors (with filtering)
- `GET /contractors/{id}` - Get specific contractor
- `PUT /contractors/{id}` - Update contractor
- `DELETE /contractors/{id}` - Delete contractor
- `GET /contractors/specialty/{specialty}` - Get contractors by specialty
- `GET /contractors/stats/summary` - Get contractor summary statistics
- `GET /contractors/{id}/maintenance-requests` - Get maintenance requests for contractor

#### Violations
- `POST /violations/` - Create a new violation
- `GET /violations/` - List all violations (with filtering)
- `GET /violations/{id}` - Get specific violation
- `PUT /violations/{id}` - Update violation
- `DELETE /violations/{id}` - Delete violation
- `GET /violations/unit/{unit_id}` - Get violations by unit
- `GET /violations/resident/{resident_id}` - Get violations by resident
- `GET /violations/stats/summary` - Get violation summary statistics

## 🔧 Usage Examples

### Create a Contractor
```bash
curl -X POST "http://localhost:8000/contractors/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Smith",
    "company": "Smith Plumbing",
    "email": "john@smithplumbing.com",
    "phone": "555-123-4567",
    "specialties": ["plumbing", "hvac"],
    "rating": 4.5,
    "license_number": "PL12345",
    "insurance_expiry": "2025-12-31"
  }'
```

### Create an Enhanced Maintenance Request
```bash
curl -X POST "http://localhost:8000/maintenance-enhanced/requests/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Fix leaking faucet",
    "description": "The kitchen faucet is leaking heavily.",
    "category": "plumbing",
    "priority": "high",
    "unit_id": "<unit-uuid>",
    "property_id": "<property-uuid>",
    "resident_id": "<resident-uuid>",
    "created_by": "<user-uuid>"
  }'
```

### Create a Maintenance Work Log
```bash
curl -X POST "http://localhost:8000/maintenance-enhanced/work-logs/" \
  -H "Content-Type: application/json" \
  -d '{
    "maintenance_request_id": "<request-uuid>",
    "worker_name": "Mike Technician",
    "work_date": "2024-07-01",
    "hours_worked": 2.5,
    "work_description": "Replaced faucet and checked for leaks.",
    "created_by": "<user-uuid>"
  }'
```

### Create a User
```bash
curl -X POST "http://localhost:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@hoa.com",
    "first_name": "Admin",
    "last_name": "User",
    "phone": "555-987-6543",
    "role": "super_admin",
    "is_active": true,
    "email_verified": true
  }'
```

### Create an Enhanced Resident
```bash
curl -X POST "http://localhost:8000/residents-enhanced/" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "<user-uuid>",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "phone": "555-111-2222",
    "unit_id": "<unit-uuid>",
    "property_id": "<property-uuid>",
    "resident_type": "owner",
    "role": "resident",
    "move_in_date": "2024-01-01",
    "emergency_contact": {"name": "Jane Doe", "phone": "555-999-8888", "relationship": "spouse"},
    "vehicle_info": [{"make": "Toyota", "model": "Camry", "year": 2020, "color": "silver", "license_plate": "ABC123"}],
    "pet_info": [{"name": "Buddy", "type": "dog", "breed": "Golden Retriever", "weight": 65}],
    "is_primary": true,
    "created_by": "<user-uuid>"
  }'
```

## 🗄️ Database Models

The system uses SQLAlchemy ORM with the following key features:

- **Relationships**: Proper foreign key relationships between entities
- **Enums**: Type-safe enums for status, types, and categories
- **Timestamps**: Automatic created_at and updated_at timestamps
- **Validation**: Pydantic schemas for request/response validation
- **Indexing**: Optimized database indexes for performance

## 🔒 Security Features

- **Input Validation**: Comprehensive Pydantic validation
- **Error Handling**: Proper HTTP status codes and error messages
- **Database Constraints**: Foreign key and check constraints
- **Type Safety**: Strong typing throughout the application

## 🚀 Deployment

### Production Setup
1. Set up PostgreSQL database
2. Configure environment variables
3. Run database migrations
4. Deploy with Gunicorn or similar WSGI server

### Docker Deployment
```bash
# Build image
docker build -t hoa-api .

# Run container
docker run -p 8000:8000 hoa-api
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions, please open an issue in the repository or contact the development team.
