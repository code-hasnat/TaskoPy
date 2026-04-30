# TaskoPy-Python

A simple and efficient task management API built with FastAPI, PostgreSQL, and JWT authentication. Perfect for managing projects and tasks with proper user authentication and authorization.

## Features

- 🔐 **JWT Authentication** - Secure user registration and login
- 📊 **Project Management** - Create, read, and delete projects
- ✅ **Task Management** - Full CRUD operations for tasks
- 🐘 **PostgreSQL Database** - Reliable data storage with proper relationships
- 🐳 **Docker Support** - Easy deployment with Docker and Docker Compose
- 📱 **Interactive API Docs** - Built-in Swagger UI for testing
- 🔒 **Role-based Access** - Users can only access their own projects and tasks
- ⚡ **Fast & Async** - Built with FastAPI for high performance

## Tech Stack

- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL
- **Authentication**: JWT (JSON Web Tokens)
- **ORM**: SQLAlchemy
- **Containerization**: Docker & Docker Compose
- **Validation**: Pydantic

## Project Structure

```
taskflow-api/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app and main configuration
│   ├── database.py          # Database connection and session
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas for validation
│   ├── auth.py              # JWT authentication logic
│   ├── dependencies.py      # Dependency injection
│   └── routers/
│       ├── __init__.py
│       ├── auth.py          # Authentication routes
│       ├── users.py         # User management routes
│       ├── projects.py      # Project management routes
│       └── tasks.py         # Task management routes
├── .env                     # Environment variables
├── .gitignore
├── requirements.txt         # Python dependencies
├── docker-compose.yml       # Docker services configuration
├── Dockerfile              # Docker image configuration
└── README.md               # This file
```

## Quick Start

### Option 1: Using Docker (Recommended)

1. **Clone and setup:**
```bash
git clone <your-repo-url>
cd taskflow-api
```

2. **Create environment file:**
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. **Start the application:**
```bash
docker-compose up -d
```

4. **Access the API:**
- API: http://localhost:8000
- Documentation: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc

### Option 2: Local Development

1. **Prerequisites:**
- Python 3.11+
- PostgreSQL 13+

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Register a new user |
| POST | `/auth/login` | Login user and get JWT token |

### Users

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/users/me` | Get current user information |
| GET | `/users/{user_id}` | Get user by ID |

### Projects

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/projects/` | Create a new project |
| GET | `/projects/` | Get all user's projects |
| GET | `/projects/{project_id}` | Get project by ID |
| DELETE | `/projects/{project_id}` | Delete a project |

### Tasks

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/tasks/` | Create a new task |
| GET | `/tasks/` | Get all tasks (with optional project_id filter) |
| GET | `/tasks/{task_id}` | Get task by ID |
| PUT | `/tasks/{task_id}` | Update a task |
| DELETE | `/tasks/{task_id}` | Delete a task |

## Data Models

### User
- `id`: Integer (Primary Key)
- `email`: String (Unique)
- `username`: String (Unique)
- `hashed_password`: String
- `is_active`: Boolean
- `created_at`: DateTime

### Project
- `id`: Integer (Primary Key)
- `name`: String
- `description`: Text (Optional)
- `owner_id`: Integer (Foreign Key → User)
- `created_at`: DateTime

### Task
- `id`: Integer (Primary Key)
- `title`: String
- `description`: Text (Optional)
- `status`: Enum (`todo`, `in_progress`, `completed`)
- `priority`: Enum (`low`, `medium`, `high`)
- `project_id`: Integer (Foreign Key → Project)
- `assignee_id`: Integer (Foreign Key → User, Optional)
- `created_at`: DateTime
- `updated_at`: DateTime

## Development

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest
```

### Database Migrations

If you need to modify the database schema:

```bash
# Install alembic
pip install alembic

# Initialize alembic (if not already done)
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Add new column"

# Apply migration
alembic upgrade head
```

### Code Formatting

```bash
# Install formatting tools
pip install black isort

# Format code
black .
isort .
```
## Security Features

- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: Passwords are hashed using bcrypt
- **CORS Protection**: Configurable CORS middleware
- **Input Validation**: Pydantic models validate all inputs
- **Authorization**: Users can only access their own resources
- **SQL Injection Protection**: SQLAlchemy ORM prevents SQL injection


### Production Considerations

1. **Change default secrets**: Update `SECRET_KEY` in production
2. **Use environment variables**: Never hardcode sensitive data
3. **Database security**: Use strong database credentials
4. **HTTPS**: Always use HTTPS in production
5. **Rate limiting**: Consider adding rate limiting middleware
6. **Monitoring**: Add logging and monitoring

## Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/yourusername/taskflow-api/issues) page
2. Create a new issue with detailed description
3. Include error logs and system information

## Roadmap

- [x] Add task dependencies
- [ ] Implement task comments
- [ ] Add file attachments
- [ ] Team collaboration features
- [ ] Task time tracking
- [ ] Email notifications
- [ ] API rate limiting
- [ ] Advanced filtering and search
- [ ] Task templates
- [ ] Project analytics dashboard