# E-commerce Backend System using FastAPI

This project is a fully functional backend system for an e-commerce platform built using **FastAPI**. 
It supports user registration, authentication, product management, cart operations, order processing, and email-based password reset. 
The system follows a modular architecture and uses JWT for secure authentication.

---

## 🚀 Tech Stack

* **FastAPI** – Web framework for building APIs
* **PostgreSQL** – Relational database
* **SQLAlchemy** – ORM for database interaction
* **Alembic** – Database migration tool
* **Pydantic** – Data validation and parsing
* **JWT (PyJWT)** – Authentication tokens
* **SMTP (Gmail)** – Email service for password reset

---

## 📁 Project Structure

```
app/
├── auth/           # User authentication, JWT, password reset
├── products/       # Admin and public product APIs
├── cart/           # Cart functionality
├── checkout/       # Order creation via checkout
├── orders/         # Order history and details
├── core/           # DB connection and config
├── utils/          # Email service and helpers
alembic/             # DB migrations
.env                 # Environment variables
main.py              # Entry point
```

---

## ⚙️ Features

### 👤 User Authentication

* Signup and signin with JWT
* Role-based access control (admin/user)
* Password hashing using bcrypt
* Password reset via email link (SMTP)

### 🛍 Product Management

* Admin can create, update, delete products
* Public users can view, search, and filter products

### 🛒 Cart System

* Add to cart, update quantity, remove items
* Cart tied to authenticated user

### 💳 Checkout & Orders

* Dummy payment simulation
* Converts cart to order
* Tracks order history and details

### 📧 Email Integration

* Forgot password via email link
* Reset password with secure token

---

## 🗃 Database Schema (PostgreSQL)

Tables:

* **users** – user\_id, email, password, role
* **products** – id, name, description, price, stock, category
* **cart** – user\_id, product\_id, quantity
* **orders** – user\_id, total\_amount, status, created\_at
* **order\_items** – order\_id, product\_id, quantity, price
* **password\_reset\_tokens** – user\_id, token, expiration, used

---

## 🔐 Authentication & Security

* JWT-based token authentication
* Role checks using FastAPI dependencies
* Passwords stored as bcrypt hashes
* Secure, expiring password reset tokens

---

## 🔄 Alembic Migrations

### Initialize Alembic

```
alembic init alembic
```

### Configure DB in `alembic.ini`

```
sqlalchemy.url = postgresql://postgres:yourpassword@localhost:5432/ecommerce_db
```

### Generate and Apply Migrations

```
alembic revision --autogenerate -m "Add product table"
alembic upgrade head
```

---

## 📬 Running the Project

### 1. Create and activate virtual environment

```
python -m venv venv
source venv/bin/activate  # Or venv\Scripts\activate on Windows
```

### 2. Install dependencies

```
pip install -r requirements.txt
```

### 3. Set up `.env`

```
DATABASE_URL=postgresql://postgres:password@localhost:5432/ecommerce_db
SECRET_KEY=your_secret_key
ACCESS_TOKEN_EXPIRE_MINUTES=30
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=youremail@gmail.com
MAIL_PASSWORD=yourapppassword
MAIL_FROM=youremail@gmail.com
```

### 4. Run migrations

```
alembic upgrade head
```

### 5. Run the server

```
uvicorn app.main:app --reload
```

Access docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 📮 API Testing

* Full Postman collection available: `ecommerce_fastapi_postman_collection.json`
* Swagger UI auto-generated at `/docs`

---

