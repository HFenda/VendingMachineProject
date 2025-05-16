# Vending Machine – FastAPI + React/Next.js

## 📌 Overview

This repository contains a full-stack vending machine web application built as part of my software engineering internship and academic project. It demonstrates backend API development, frontend design, and implementation of automated testing (unit, integration, performance, and security).

---

## 🏗️ Project Structure

```bash
VendingMachineProject/
├── backend/                   # FastAPI application (Python)
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── routers/
│   │   ├── items.py
│   │   └── users.py
│   ├── integration_tests/
│   │   ├── test_items.py
│   │   └── test_users.py
│   └── integration_tests/
│       ├── test_add_item.py
│       ├── test_login.py
│       └── ...
├── frontend/                  # React + Next.js app (TypeScript)
│   └── ...
└── README.md
```

---

⚙️ **Technologies Used**

| Layer       | Tech Stack                          |
|-------------|-------------------------------------|
| Frontend    | Next.js, React, TypeScript, Tailwind CSS |
| Backend     | FastAPI, SQLAlchemy, PostgreSQL     |
| Testing     | pytest, FastAPI TestClient, Selenium, JMeter, OWASP ZAP |
| Tools       | Git, Postman, VSCode |

---

## 🚀 **Features**

### 🔹 Backend (FastAPI)
- CRUD operations for items (products)
- User login and role-based actions
- Purchasing and revenue tracking logic
- SQLAlchemy ORM for PostgreSQL database
- Exception handling and clean API responses

### 🔹 Frontend (Next.js)
- Clean and responsive UI
- Item list display and filtering
- Forms for adding/editing items
- Purchase logic and role management
- Admin/user view separation

---

## 📦 **Setup Instructions**

### 🔹 Backend (FastAPI)
```bash
   cd backend
   poetry install
   poetry run uvicorn main:app --reload
```
Make sure PostgreSQL is running and the connection string in database.py is set correctly.

### 🔹 Frontend (Next.js)
```bash
   cd frontend
   npm install
   npm run dev
```

---

## ✅ **Testing Overview**

### 1. 🧪 Unit & Integration Testing (pytest)
- Covered major endpoints using FastAPI TestClient
- Tested input validation, CRUD logic, error handling
- Verified DB interactions (in-memory PostgreSQL setup)

### 2. ⚡ Performance Testing (JMeter)
- Load tested GET, POST, DELETE endpoints
- Simulated 50, 100, and 200 users
- Measured response time, throughput, and scalability

**📊 Example Throughput Summary:**

| Method  | Users | Avg. Time (ms) | Max Time (ms) | Throughput (req/s) |
|---------|-------|----------------|---------------|--------------------|
| GET     | 50    | 135            | 300           | 4.7                |
| POST    | 100   | 410            | 950           | 4.5                |
| DELETE  | 200   | 460            | 1200          | 7.3                |

📈 *Graphs and screenshots are included in the documentation folder.*

### 3. 🔐 Security Testing (OWASP ZAP)
- Manual and automated scans against SQLi, XSS
- No critical vulnerabilities detected
- Recommendations documented for safer auth/storage

---

## 📚 **Documentation**
Full documentation includes:
- 📄 Project goal and requirements
- ⚙️ Strategy for test automation
- 🧪 Detailed results (tables + graphs)
- 🔐 Security threats and mitigation
- 📌 Recommendations for improvement

Link: https://docs.google.com/document/d/1G36DLFKej4E9RbmQjXXkdt_7UqTfAFUIIGTxOHHrBGI/edit?usp=sharing

---

## 💡 **Learnings & Highlights**
- Practical use of FastAPI dependency injection and exception handling
- Integration of testing at multiple levels (unit → performance)
- Using JMeter for real-world load simulation
- Writing secure and modular full-stack applications

---

## 📬 **Contact**

- **LinkedIn**: [Harun Aliefendic](https://www.linkedin.com/in/harun-aliefendic/)
- **Email**: aliefendic.harun.21@size.ba
- **GitHub**: [@HFenda](https://github.com/HFenda)
