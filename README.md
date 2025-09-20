# Digital Store - Local Development Guide

## 🚀 Quick Start

### Prerequisites
- Docker Desktop installed and running
- Git

### 1. Clone and Setup
```bash
git clone <repository-url>
cd digital_store
```

### 2. Start Development Environment
```bash
# Start all services
docker-compose -f docker-compose.local.yml up -d

# Check if all services are running
docker-compose -f docker-compose.local.yml ps
```

### 3. Create Superuser
You can create a superuser in two ways:

#### Method A: Via Command Line
```bash
docker-compose -f docker-compose.local.yml exec web python manage.py createsuperuser
```

#### Method B: Via API Endpoint
```bash
### Create Superuser via API

For convenience, you can create a superuser account via API:

```bash
curl -X POST http://localhost:8000/api/create-superuser/ \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "09123456789",
    "email": "admin@example.com", 
    "password": "admin123456",
    "fullName": "Admin User"
  }'
```

**Note**: This project uses a custom User model where `phone` is the username field (not `username`).

Or visit the Swagger UI at http://localhost:8000/swagger/ and use the interactive documentation.
```

### 4. Access Your Application
- **Django App**: http://localhost:8000
- **Django Admin**: http://localhost:8000/admin
- **API Documentation**: http://localhost:8000/api/schema/swagger-ui/
- **Flower (Celery Monitor)**: http://localhost:5555 (admin/admin)

---

## 📋 Available Commands

### Container Management
```bash
# Start services
docker-compose -f docker-compose.local.yml up -d

# Stop services
docker-compose -f docker-compose.local.yml down

# Rebuild and start (after code changes to dependencies)
docker-compose -f docker-compose.local.yml up --build -d

# View logs
docker-compose -f docker-compose.local.yml logs -f

# View logs for specific service
docker-compose -f docker-compose.local.yml logs -f web
```

### Django Management
```bash
# Run migrations
docker-compose -f docker-compose.local.yml exec web python manage.py migrate

# Create migrations
docker-compose -f docker-compose.local.yml exec web python manage.py makemigrations

# Collect static files
docker-compose -f docker-compose.local.yml exec web python manage.py collectstatic

# Django shell
docker-compose -f docker-compose.local.yml exec web python manage.py shell

# Run tests
docker-compose -f docker-compose.local.yml exec web python manage.py test
```

### Database Operations
```bash
# Access PostgreSQL
docker-compose -f docker-compose.local.yml exec db psql -U postgres -d digital_store_dev

# Create database backup
docker-compose -f docker-compose.local.yml exec db pg_dump -U postgres digital_store_dev > backup.sql

# Restore database
docker-compose -f docker-compose.local.yml exec -T db psql -U postgres digital_store_dev < backup.sql
```

---

## 🛠️ Development Workflow

### Making Code Changes
1. **Python/Django changes**: Changes are automatically reflected (volume mounted)
2. **Requirements changes**: Rebuild containers
   ```bash
   docker-compose -f docker-compose.local.yml up --build -d
   ```
3. **Database schema changes**: Run migrations
   ```bash
   docker-compose -f docker-compose.local.yml exec web python manage.py makemigrations
   docker-compose -f docker-compose.local.yml exec web python manage.py migrate
   ```

### Debugging
```bash
# View real-time logs
docker-compose -f docker-compose.local.yml logs -f web

# Access container shell
docker-compose -f docker-compose.local.yml exec web bash

# Check container status
docker-compose -f docker-compose.local.yml ps
```

---

## 📦 Services Overview

| Service | Description | Port | Health Check |
|---------|-------------|------|--------------|
| **web** | Django Application | 8000 | ✅ |
| **db** | PostgreSQL Database | 5432 | ✅ |
| **redis** | Cache & Message Broker | 6380 | ✅ |
| **celery_worker** | Background Tasks | - | ✅ |
| **celery_beat** | Scheduled Tasks | - | ✅ |
| **flower** | Task Monitor | 5555 | ✅ |

---

## 🗃️ Database Connection

### PostgreSQL Details
- **Host**: localhost
- **Port**: 5432
- **Database**: digital_store_dev
- **Username**: postgres
- **Password**: postgres

### Redis Details
- **Host**: localhost  
- **Port**: 6380

---

## 🔧 Configuration

### Environment Variables
Local settings are in `.env.local`:
- `DEBUG=True`
- Development database URLs
- Local Redis configuration
- Test API keys

### Key Features Enabled
- ✅ Debug mode
- ✅ Live code reloading
- ✅ PostgreSQL database
- ✅ Redis caching
- ✅ Celery background tasks
- ✅ Administrative interface
- ✅ API documentation

---

## 🚨 Troubleshooting

### Common Issues

#### Containers Won't Start
```bash
# Check for port conflicts
docker-compose -f docker-compose.local.yml down
docker-compose -f docker-compose.local.yml up -d

# Check logs for errors
docker-compose -f docker-compose.local.yml logs
```

#### Database Connection Issues
```bash
# Ensure database is healthy
docker-compose -f docker-compose.local.yml ps

# Reset database
docker-compose -f docker-compose.local.yml down -v
docker-compose -f docker-compose.local.yml up -d
```

#### Permission Issues
```bash
# On Linux/Mac, fix file permissions
sudo chown -R $USER:$USER .
```

#### Clean Reset
```bash
# Complete reset (removes all data)
docker-compose -f docker-compose.local.yml down -v
docker system prune -f
docker-compose -f docker-compose.local.yml up --build -d
```

### Performance Issues
- Ensure Docker has sufficient memory (4GB+ recommended)
- Close unnecessary applications
- Use SSD storage for better performance

---

## 🔍 Monitoring & Logs

### Health Checks
All services include health checks that ensure proper startup order:
```bash
# Check service health
docker-compose -f docker-compose.local.yml ps
```

### Flower Dashboard
Monitor Celery tasks at http://localhost:5555
- Username: `admin`
- Password: `admin`

### Log Aggregation
```bash
# All services
docker-compose -f docker-compose.local.yml logs -f

# Specific service with timestamps
docker-compose -f docker-compose.local.yml logs -f -t web
```

---

## 📝 API Documentation

### Swagger UI
Visit http://localhost:8000/api/schema/swagger-ui/ for interactive API documentation.

### Key Endpoints
- **Admin**: `/admin/`
- **API Root**: `/api/`
- **Create Superuser**: `/api/create-superuser/`
- **Schema**: `/api/schema/`
- **Payment**: `/payment/`

---

## 🧪 Testing

### Run Tests
```bash
# All tests
docker-compose -f docker-compose.local.yml exec web python manage.py test

# Specific app
docker-compose -f docker-compose.local.yml exec web python manage.py test store

# With coverage
docker-compose -f docker-compose.local.yml exec web coverage run --source='.' manage.py test
docker-compose -f docker-compose.local.yml exec web coverage report
```

---

## 🤝 Contributing

1. Make your changes
2. Run tests
3. Check code style
4. Submit pull request

### Code Quality
```bash
# Format code
docker-compose -f docker-compose.local.yml exec web black .

# Check migrations
docker-compose -f docker-compose.local.yml exec web python manage.py makemigrations --check --dry-run
```

---

## 📞 Support

If you encounter issues:
1. Check this README
2. Check container logs
3. Try a clean reset
4. Contact the development team

Happy coding! 🚀