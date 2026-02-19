# Fitness Booking API

A simple **Booking API** for a fictional fitness studio built with **Python + FastAPI**.  
This API allows users to sign up, log in, view classes, create classes, and book fitness sessions.

---

## 📌 Tech Stack

- **Language:** Python  
- **Framework:** FastAPI  
- **Database:** SQLite  
- **ORM:** SQLAlchemy (optional)  
- **Authentication:** JWT token-based authentication  
- **Environment:** Python virtual environment (`venv`)

---

## 🚀 Features

- User authentication (Sign Up / Log In)
- Create new fitness classes (Admin/User)
- View all upcoming classes
- Book available classes
- View your own bookings
- Overbooking prevention
- Timezone aware (all times in IST)

---
## 🔐 Authentication Using JWT

JWT (JSON Web Token) is used to secure the application.

### 🔄 Authentication Flow
1. User logs in using email and password
2. Server validates credentials
3. Server generates a JWT token
4. Token is returned to the client
5. Client sends the token in request headers
6. FastAPI verifies the token before allowing access
7. If token is invalid or expired, request is rejected with 401 Unauthorized
