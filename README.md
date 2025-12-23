# User Activity Tracker

A production-ready Python backend API for recording, storing, and querying user activity events. Built with FastAPI and SQLAlchemy, this service provides a scalable solution for tracking user interactions across applications.

## Features

- **Event Ingestion**: Record user events with structured data (user_id, event_type, timestamp, metadata)
- **Flexible Querying**: Filter events by user, event type, and date ranges
- **RESTful API**: Clean, well-documented endpoints following REST principles
- **Auto-generated Documentation**: Interactive OpenAPI (Swagger) docs at `/docs`
- **SQLite Database**: Simple setup with SQLAlchemy ORM (easily swappable for PostgreSQL/MySQL)
- **Data Validation**: Request/response validation using Pydantic schemas
- **Error Handling**: Comprehensive error handling with meaningful HTTP status codes

## Project Structure

```
user-activity-tracker/
├── app/
│   ├── main.py          # FastAPI application entry point
│   ├── database.py      # Database configuration and session management
│   ├── models.py        # SQLAlchemy models
│   ├── schemas.py       # Pydantic schemas for validation
│   └── routes.py        # API endpoint definitions
├── requirements.txt     # Python dependencies
├── README.md           # Project documentation
└── .env.example        # Environment variables template
```

## Tech Stack

- **Python 3.8+**
- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **Pydantic**: Data validation using Python type annotations
- **Uvicorn**: ASGI server for running the application
- **SQLite**: Lightweight database (default)

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd user-activity-tracker
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. (Optional) Configure environment variables:
```bash
cp .env.example .env
# Edit .env if you want to customize the database URL
```

### Running the Application

Start the development server:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

- **Interactive API Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## API Documentation

### Base URL
```
http://localhost:8000/api/v1
```

### Endpoints

#### 1. Create Event
Record a new user activity event.

**POST** `/api/v1/events`

**Request Body:**
```json
{
  "user_id": "user_123",
  "event_type": "login",
  "timestamp": "2025-01-15T10:30:00Z",
  "metadata": {
    "ip_address": "192.168.1.1",
    "user_agent": "Mozilla/5.0"
  }
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "user_id": "user_123",
  "event_type": "login",
  "timestamp": "2025-01-15T10:30:00Z",
  "metadata": {
    "ip_address": "192.168.1.1",
    "user_agent": "Mozilla/5.0"
  }
}
```

**cURL Example:**
```bash
curl -X POST "http://localhost:8000/api/v1/events" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_123",
    "event_type": "login",
    "metadata": {"ip_address": "192.168.1.1"}
  }'
```

#### 2. Get All Events (with filters)
Retrieve events with optional filtering.

**GET** `/api/v1/events`

**Query Parameters:**
- `user_id` (optional): Filter by user ID
- `event_type` (optional): Filter by event type
- `start_date` (optional): Filter events after this date (ISO 8601)
- `end_date` (optional): Filter events before this date (ISO 8601)
- `limit` (optional, default: 100): Max number of results (1-1000)
- `offset` (optional, default: 0): Number of results to skip

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "user_id": "user_123",
    "event_type": "login",
    "timestamp": "2025-01-15T10:30:00Z",
    "metadata": {"ip_address": "192.168.1.1"}
  },
  {
    "id": 2,
    "user_id": "user_123",
    "event_type": "page_view",
    "timestamp": "2025-01-15T10:31:00Z",
    "metadata": {"page": "/dashboard"}
  }
]
```

**cURL Examples:**

Get all events:
```bash
curl "http://localhost:8000/api/v1/events"
```

Filter by user:
```bash
curl "http://localhost:8000/api/v1/events?user_id=user_123"
```

Filter by event type:
```bash
curl "http://localhost:8000/api/v1/events?event_type=login"
```

Filter by date range:
```bash
curl "http://localhost:8000/api/v1/events?start_date=2025-01-01T00:00:00Z&end_date=2025-01-31T23:59:59Z"
```

Combined filters with pagination:
```bash
curl "http://localhost:8000/api/v1/events?user_id=user_123&event_type=page_view&limit=50&offset=0"
```

#### 3. Get Single Event
Retrieve a specific event by ID.

**GET** `/api/v1/events/{event_id}`

**Response:** `200 OK`
```json
{
  "id": 1,
  "user_id": "user_123",
  "event_type": "login",
  "timestamp": "2025-01-15T10:30:00Z",
  "metadata": {"ip_address": "192.168.1.1"}
}
```

**cURL Example:**
```bash
curl "http://localhost:8000/api/v1/events/1"
```

#### 4. Get User Events
Retrieve all events for a specific user.

**GET** `/api/v1/users/{user_id}/events`

**Query Parameters:**
- `event_type` (optional): Filter by event type
- `limit` (optional, default: 100)
- `offset` (optional, default: 0)

**cURL Example:**
```bash
curl "http://localhost:8000/api/v1/users/user_123/events?limit=50"
```

### Common Event Types

- `login` - User authentication
- `logout` - User session end
- `page_view` - Page navigation
- `click` - UI interaction
- `form_submit` - Form submission
- `api_call` - API request
- `error` - Error occurrence

## Example Usage Workflow

```bash
# 1. Record a login event
curl -X POST "http://localhost:8000/api/v1/events" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_456",
    "event_type": "login",
    "metadata": {"method": "oauth", "provider": "google"}
  }'

# 2. Record a page view
curl -X POST "http://localhost:8000/api/v1/events" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_456",
    "event_type": "page_view",
    "metadata": {"page": "/dashboard", "duration_ms": 5000}
  }'

# 3. Record a button click
curl -X POST "http://localhost:8000/api/v1/events" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_456",
    "event_type": "click",
    "metadata": {"button_id": "export-data", "page": "/dashboard"}
  }'

# 4. Query all events for this user
curl "http://localhost:8000/api/v1/users/user_456/events"

# 5. Query only login events
curl "http://localhost:8000/api/v1/events?event_type=login"
```

## Why This Demonstrates Python Backend Skills

This project showcases essential backend development capabilities:

1. **RESTful API Design**: Well-structured endpoints following REST principles and HTTP standards

2. **Database Management**:
   - SQLAlchemy ORM for database abstraction
   - Proper indexing on frequently queried fields
   - Efficient query building with filtering and pagination

3. **Data Validation**:
   - Pydantic schemas for request/response validation
   - Type safety and automatic data serialization

4. **Modern Python Practices**:
   - Type hints for code clarity
   - Async context managers for resource management
   - Dependency injection pattern

5. **Production-Ready Features**:
   - CORS middleware for cross-origin requests
   - Health check endpoints
   - Error handling and meaningful HTTP status codes
   - Auto-generated OpenAPI documentation

6. **Scalability Considerations**:
   - Pagination support for large datasets
   - Database indexing for query performance
   - Configurable through environment variables
   - Easy migration path to production databases (PostgreSQL/MySQL)

7. **Clean Architecture**:
   - Separation of concerns (routes, models, schemas, database)
   - Modular code structure
   - Follows Python best practices and PEP 8

## Testing

You can test the API using:

1. **Interactive Swagger UI**: http://localhost:8000/docs
2. **cURL**: See examples above
3. **Postman/Insomnia**: Import the OpenAPI schema from `/openapi.json`
4. **Python requests library**:

```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/events",
    json={
        "user_id": "test_user",
        "event_type": "login",
        "metadata": {"source": "python_script"}
    }
)
print(response.json())
```

## Future Enhancements

Potential improvements for production deployment:

- Authentication & authorization (JWT tokens, API keys)
- Rate limiting
- Event aggregation and analytics endpoints
- Real-time event streaming (WebSockets)
- Database migrations with Alembic
- Unit and integration tests
- Docker containerization
- CI/CD pipeline
- Monitoring and logging
- Caching layer (Redis)

## License

MIT License
