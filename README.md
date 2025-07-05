# HOA Management System API

A comprehensive FastAPI backend for managing Homeowners Association operations with Neon PostgreSQL database support.

## 🚀 Features

- **Property Management**: Manage properties, units, and residents
- **Financial Tracking**: Handle payments, financial accounts, and management fees
- **Maintenance Requests**: Track maintenance requests with priorities and status
- **Violation Management**: Manage community violations and fines
- **Meeting Management**: Schedule and track board meetings
- **Document Management**: Store and manage HOA documents
- **Service Provider Management**: Track contractors and service providers

## 🏗️ Architecture

```
app/
├── database.py          # Database connection and session management
├── main.py             # FastAPI application entry point
├── models.py           # SQLAlchemy models for all entities
├── schemas.py          # Pydantic schemas for request/response validation
└── routes/             # API route modules
    ├── properties.py   # Property management endpoints
    ├── units.py        # Unit management endpoints
    ├── residents.py    # Resident management endpoints
    ├── payments.py     # Payment tracking endpoints
    ├── maintenance.py  # Maintenance request endpoints
    └── violations.py   # Violation management endpoints
```

## 📋 Database Schema

The system includes the following main entities:

### Core Entities
- **Properties**: HOA properties with details like name, address, total units
- **Units**: Individual units within properties with specifications
- **Residents**: People living in units (owners, tenants, board members)
- **Payments**: Financial transactions and fee payments
- **Maintenance Requests**: Service requests with priorities and tracking
- **Violations**: Community rule violations and enforcement
- **Meetings**: Board and community meetings
- **Documents**: File storage and management
- **Service Providers**: Contractors and service companies
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

#### Residents
- `POST /residents/` - Create a new resident
- `GET /residents/` - List all residents (with filtering)
- `GET /residents/{id}` - Get specific resident
- `PUT /residents/{id}` - Update resident
- `DELETE /residents/{id}` - Delete resident
- `GET /residents/unit/{unit_id}` - Get residents by unit
- `GET /residents/{id}/stats` - Get resident statistics

#### Payments
- `POST /payments/` - Create a new payment
- `GET /payments/` - List all payments (with filtering)
- `GET /payments/{id}` - Get specific payment
- `PUT /payments/{id}` - Update payment
- `DELETE /payments/{id}` - Delete payment
- `GET /payments/resident/{resident_id}` - Get payments by resident
- `GET /payments/unit/{unit_id}` - Get payments by unit
- `GET /payments/stats/summary` - Get payment summary statistics

#### Maintenance Requests
- `POST /maintenance/` - Create a new maintenance request
- `GET /maintenance/` - List all requests (with filtering)
- `GET /maintenance/{id}` - Get specific request
- `PUT /maintenance/{id}` - Update request
- `DELETE /maintenance/{id}` - Delete request
- `GET /maintenance/unit/{unit_id}` - Get requests by unit
- `GET /maintenance/resident/{resident_id}` - Get requests by resident
- `GET /maintenance/stats/summary` - Get maintenance summary statistics

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

### Create a Property
```bash
curl -X POST "http://localhost:8000/properties/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Sunset Apartments",
    "address": "123 Main Street, Downtown",
    "total_units": 50,
    "property_type": "apartment",
    "year_built": 2020
  }'
```

### Create a Unit
```bash
curl -X POST "http://localhost:8000/units/" \
  -H "Content-Type: application/json" \
  -d '{
    "property_id": 1,
    "unit_number": "101",
    "unit_type": "1-bedroom",
    "square_feet": 750,
    "bedrooms": 1,
    "bathrooms": 1.0,
    "monthly_fee": 1200.00
  }'
```

### Create a Resident
```bash
curl -X POST "http://localhost:8000/residents/" \
  -H "Content-Type: application/json" \
  -d '{
    "unit_id": 1,
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@email.com",
    "phone": "555-123-4567",
    "resident_type": "owner",
    "move_in_date": "2023-01-15",
    "emergency_contact_name": "Jane Doe",
    "emergency_contact_phone": "555-987-6543"
  }'
```

### Create a Payment
```bash
curl -X POST "http://localhost:8000/payments/" \
  -H "Content-Type: application/json" \
  -d '{
    "resident_id": 1,
    "unit_id": 1,
    "amount": 1200.00,
    "payment_type": "monthly_fee",
    "payment_method": "online",
    "payment_date": "2023-12-01",
    "due_date": "2023-12-01",
    "status": "paid",
    "notes": "Monthly HOA fee"
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
