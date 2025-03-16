# Homework 2 – Flask + MongoDB + Socket.IO

This repository demonstrates a **Flask** application that implements:

1. **User Authentication** (Login, Logout, Registration)  
2. **Password Hashing** for secure credential storage  
3. **Profile Page** restricted to authenticated users  
4. **Change Password** feature  
5. **Socket.IO** for real-time notifications (challenging part)  
6. **MongoDB** integration for storing user data  
7. **Minimal Frontend** with HTML/CSS

---

## 1. Project Overview

- **Basic Requirements**:
  - Listen on `localhost:5000`.
  - Render login form at `/`.
  - Redirect to `/profile` on successful authentication; show profile only if logged in.
  - Store credentials in MongoDB (hashed with Werkzeug).

- **Advanced Features**:
  - Registration with hashed passwords.
  - Logout route to clear sessions.
  - Change Password route.
  - Profile page showing user info.

- **Challenging/Optional**:
  - **Socket.IO** broadcast on new user registration.  
    All connected users receive a “New user has joined” alert in real time.

---

## 2. Tech Stack

- **Python 3.10+** (version may vary)
- **Flask 3.x**
- **MongoDB** 
- **Flask-SocketIO** for real-time functionality
- **Werkzeug** for password hashing
- **HTML/CSS** templates in `templates/` and `static/`

---

## 3. Directory Structure
```
    ├── app.py # Main Flask + Socket.IO 
    ├── requirements.txt # Python dependencies 
    ├── static/ │ 
        └── style.css # Basic CSS for the templates 
    └── templates/ 
        ├── base.html # Base layout with nav, Socket.IO client script 
        ├── login.html # Login form 
        ├── register.html # Registration form 
        ├── profile.html # User profile page 
        └── change_password.html # Form to update password
```

## install dependancies 
```
pip install -r requirements.txt

```