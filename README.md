# 🧪 Pytest-BDD + Requests + JSON Schema Demo

This repository is a **demo project** to showcase automation skills in **API testing** using Python.

---

## 🚀 Tech stack
- **[pytest](https://docs.pytest.org/)** — test runner  
- **[pytest-bdd](https://pytest-bdd.readthedocs.io/)** — BDD layer on top of pytest  
- **[requests](https://requests.readthedocs.io/)** — HTTP client  
- **[jsonschema](https://python-jsonschema.readthedocs.io/)** — JSON Schema validation  
- **[dotenv](https://pypi.org/project/python-dotenv/)** — environment variables loader  

---

## 📂 Project structure
```text
pytest-bdd-reqres/
├─ tests/
│  ├─ features/        # Feature files (BDD scenarios)
│  ├─ schemas/         # JSON schemas
│  ├─ steps/           # Step definitions
│  └─ conftest.py      # Fixtures & config
├─ requirements.txt    # Dependencies
├─ pytest.ini          # Pytest config
└─ README.md
```
## 🧪 How to run
Create a virtual environment and install dependencies:
```
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```
Run tests:
```
pytest -q
```
Generate JUnit report:
```
pytest --junit-xml=reports/junit.xml
```
## 🔧 Environment variables
Optional .env file:
```
BASE_URL=https://reqres.in
```
## 🎯 Purpose

This repository was created for demonstration purposes only to highlight skills in:

writing BDD-style API tests with pytest-bdd

working with REST APIs via requests

validating response structure with JSON Schema

setting up CI pipelines with JUnit reports
