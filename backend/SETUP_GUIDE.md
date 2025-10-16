# Complete Setup Guide

## Step-by-Step Installation

### Step 1: Create Project Structure

Create the following directory structure:

```
fastapi-auth-backend/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   ├── security.py
│   │   └── dependencies.py
│   └── users/
│       ├── __init__.py
│       └── routes.py
├── tests/
│   ├── __init__.py
│   └── test_auth.py
├── .env
├── .gitignore
├── requirements.txt
├── pytest.ini
└── README.md
```

### Step 4: Install Python (if needed)

Make sure you have Python 3.8+ installed:
```bash
python --version
```

If not installed, download from [python.org](https://www.python.org/downloads/)

### Step 5: Create Virtual Environment

```bash
# Navigate to project directory
cd fastapi-auth-backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate

# You should see (venv) in your terminal prompt
```

### Step 6: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 7: Generate Secret Key

Generate a secure secret key for JWT tokens:

```bash
# Using Python
python -c "import secrets; print(secrets.token_hex(32))"

# Or using OpenSSL (if available)
openssl rand -hex 32
```

Copy the generated key.

### Step 8: Configure Environment Variables

Create `.env` file and add:

```
DATABASE_URL=sqlite:///./app.db
SECRET_KEY=paste_your_generated_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
APP_NAME=Mobile Auth API
DEBUG=True
```

### Step 9: Verify Installation

Check if everything is installed correctly:

```bash
pip list
```

You should see all the packages from requirements.txt.

### Step 10: Run the Application

```bash
# Start the server
uvicorn app.main:app --reload

# You should see output like:
# INFO:     Uvicorn running on http://127.0.0.1:8000
# INFO:     Application startup complete.
```

### Step 11: Test the API

Open your browser and navigate to:
- http://localhost:8000 (health check)
- http://localhost:8000/docs (Swagger documentation)

### Step 12: Run Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=app tests/
```

## Quick Test Commands

### Test Registration
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "password": "Test1234!"
  }'
```

### Test Login
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "Test1234!"
  }'
```

Save the `access_token` from the response.

### Test Protected Route
```bash
curl -X GET "http://localhost:8000/users/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE"
```

## Troubleshooting

### Issue: "No module named 'app'"

**Solution:** Make sure you're running commands from the project root directory and `__init__.py` files exist.

### Issue: "pydantic_settings not found"

**Solution:** Update pydantic:
```bash
pip install --upgrade pydantic[email]
```

### Issue: "Database is locked"

**Solution:** Close any SQLite browser tools or other connections to the database.

### Issue: Port 8000 already in use

**Solution:** Use a different port:
```bash
uvicorn app.main:app --reload --port 8001
```

### Issue: CORS errors from mobile app

**Solution:** Update the CORS configuration in `app/main.py` to include your mobile app's origin.

## Next Steps

1. **Test all endpoints** using the Swagger docs at `/docs`
2. **Run the test suite** to ensure everything works
3. **Integrate with your mobile app** using the examples in README.md
4. **Deploy to production** server (see deployment section in README)
5. **Switch to PostgreSQL** for production use

## Production Checklist

Before deploying to production:

- [ ] Change `SECRET_KEY` to a secure random value
- [ ] Set `DEBUG=False` in `.env`
- [ ] Switch to PostgreSQL database
- [ ] Configure CORS to allow only your mobile app domains
- [ ] Set up HTTPS/SSL certificates
- [ ] Implement rate limiting
- [ ] Set up logging and monitoring
- [ ] Configure database backups
- [ ] Set up CI/CD pipeline
- [ ] Add health check monitoring

## Getting Help

If you encounter issues:

1. Check the error message in the terminal
2. Review the Swagger docs at `/docs`
3. Verify your `.env` configuration
4. Check that all dependencies are installed
5. Ensure virtual environment is activated
6. Review the test files for usage examples

## Common Development Tasks

### Add a new endpoint

1. Define the schema in `schemas.py`
2. Create the route in appropriate `routes.py`
3. Add tests in `tests/test_auth.py`

### Change token expiration

Update `ACCESS_TOKEN_EXPIRE_MINUTES` in `.env`

### Add new user fields

1. Add column to `models.py` User model
2. Update schemas in `schemas.py`
3. Delete old database or run migrations

### View database contents

Use DB Browser for SQLite or any SQLite viewer to inspect `app.db`

---

**You're all set!** 🎉

Your authentication backend is ready to use with your mobile app.