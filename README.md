# 🧪 Enhanced QA Portfolio - API Testing Framework

This repository is an **enhanced demo project** showcasing advanced automation skills in **API testing** using Python with modern DevOps practices.

---

## 🚀 Tech Stack
- **[pytest](https://docs.pytest.org/)** — test runner  
- **[pytest-bdd](https://pytest-bdd.readthedocs.io/)** — BDD layer on top of pytest  
- **[requests](https://requests.readthedocs.io/)** — HTTP client with retry strategy
- **[jsonschema](https://python-jsonschema.readthedocs.io/)** — JSON Schema validation  
- **[pytest-html](https://pytest-html.readthedocs.io/)** — HTML test reports
- **[pytest-xdist](https://pytest-xdist.readthedocs.io/)** — Parallel test execution
- **[allure-pytest](https://docs.qameta.io/allure/)** — Allure test reports
- **[Docker](https://www.docker.com/)** — Containerization
- **[GitHub Actions](https://github.com/features/actions)** — CI/CD pipeline

---

## 📂 Enhanced Project Structure
```text
qa_portfolio/
├─ tests/
│  ├─ features/        # BDD feature files
│  ├─ schemas/         # JSON validation schemas
│  ├─ steps/           # Step definitions
│  ├─ data/            # Test data management
│  ├─ utils/           # Utility functions
│  └─ conftest.py      # Enhanced fixtures & config
├─ reports/            # Test reports (HTML, JUnit, Allure)
├─ logs/               # Structured logging
├─ .github/workflows/  # CI/CD pipelines
├─ config.py           # Configuration management
├─ requirements.txt    # Dependencies
├─ pytest.ini          # Pytest configuration
├─ Dockerfile          # Container configuration
├─ docker-compose.yml  # Multi-container setup
└─ README.md
```

## 🧪 How to Run

### Local Development
```bash
# Create virtual environment
python3 -m venv .venv && source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest -q

# Run tests in parallel
pytest -n auto

# Generate HTML report
pytest --html=reports/report.html --self-contained-html

# Generate JUnit report
pytest --junit-xml=reports/junit.xml
```

### Docker
```bash
# Build image
docker build -t qa-portfolio:latest .

# Run tests in container
docker run --rm -v $(pwd)/reports:/app/reports -v $(pwd)/logs:/app/logs qa-portfolio:latest

# Using docker-compose
docker-compose up qa-tests
docker-compose up qa-tests-parallel
```

### CI/CD
The project includes GitHub Actions workflows for:
- **Multi-version testing** (Python 3.11, 3.12)
- **Parallel execution**
- **Docker testing**
- **Security scanning** (bandit, safety)
- **Artifact collection**

## 🔧 Configuration

### Environment Variables
```bash
BASE_URL=https://reqres.in          # API base URL
TIMEOUT=30                          # Request timeout
RETRY_COUNT=3                       # Retry attempts
RETRY_BACKOFF_FACTOR=1.0           # Retry backoff
PARALLEL_WORKERS=4                  # Parallel workers
LOG_LEVEL=INFO                      # Logging level
ENABLE_HTML_REPORT=true             # HTML reports
ENABLE_ALLURE_REPORT=true           # Allure reports
```

### Test Data Management
Test data is organized in JSON files under `tests/data/`:
- `auth_data.json` - Authentication test data
- `user_data.json` - User management test data  
- `resource_data.json` - Resource test data

## 🎯 Key Features

### ✅ **Enhanced Error Handling**
- Retry mechanism for transient failures
- Comprehensive exception handling
- Detailed error logging

### ✅ **Structured Logging**
- File and console logging
- Configurable log levels
- Request/response logging

### ✅ **Parallel Execution**
- Multi-worker test execution
- Configurable worker count
- Performance optimization

### ✅ **Advanced Reporting**
- HTML reports with screenshots
- JUnit XML for CI integration
- Allure reports for detailed analysis

### ✅ **Containerization**
- Docker support for consistent environments
- Multi-stage builds for optimization
- Docker Compose for complex scenarios

### ✅ **CI/CD Integration**
- GitHub Actions workflows
- Multi-version testing
- Security scanning
- Artifact collection

### ✅ **Configuration Management**
- Environment-based configuration
- Centralized settings
- Flexible parameterization

## 🎯 Skills Demonstrated

This enhanced repository showcases:

- **Advanced API Testing** with BDD methodology
- **Error Handling & Resilience** with retry strategies
- **Performance Optimization** with parallel execution
- **DevOps Integration** with Docker and CI/CD
- **Test Data Management** with structured data files
- **Comprehensive Reporting** with multiple formats
- **Security Best Practices** with vulnerability scanning
- **Configuration Management** with environment variables
- **Structured Logging** for debugging and monitoring
- **Modern Python Practices** with type hints and documentation
