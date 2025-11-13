# 📦 LendWise — Inventory & Checkout Manager

![Python](https://img.shields.io/badge/Python-3.9+-blue)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-orange)
![PySide6](https://img.shields.io/badge/GUI-PySide6-green)
![License](https://img.shields.io/badge/License-MIT-lightgrey)
![Status](https://img.shields.io/badge/Status-Backend_Complete-brightgreen)

---

## 👥 Team Members
- Ebunoluwa Shokefun — Backend Developer  
- Dahir Abdullahi — Logic Lead  

---

## 🧩 Introduction
**LendWise** is a lightweight inventory and checkout management system designed for libraries, schools, and small organizations.  
Existing enterprise systems are often complex or expensive — *LendWise* fills the gap with a simple, affordable, and cross-platform desktop solution.  

The system allows administrators to:
- Manage items and users easily.  
- Handle checkouts and returns.  
- Automatically track overdue fines.  
- Generate reports and insights.  

---

## 🎯 Key Objectives

🧑‍💻 Provide a user-friendly interface for managing users and inventory.
🔄 Streamline item checkout and return workflows.
⏰ Automatically detect overdue loans and apply fines.
🔐 Implement secure login and authentication for patrons and librarians.
📊 Generate administrative insights and reports.
💻 Ensure cross-platform compatibility (Windows & macOS).

---
| Feature                           | Description                                                                       |
| --------------------------------- | ---------------------------------------------------------------------------------  
| 👤 **Login & Authentication**     | Role-based access for librarians and patrons, with password hashing for security. |
| 📦 **Item Management**            | Add, edit, or remove books and resources.                                         |
| 🔄 **Checkout/Return System**     | Borrow and return items seamlessly via the GUI.                                   |
| ⏰ **Overdue Tracking**           | Automatically calculates overdue fines.                                           |
| 💰 **Fine Management**            | Track, update, and display unpaid fines.                                          |
| 🧠 **Backend ORM**                | SQLAlchemy-powered database with clean data models.                               |
| 🖥️ **Graphical Interface (GUI)** | Built with PySide6 for a responsive, modern desktop experience.                    |


---
📂 System Architecture  
LendWise/
│
├── backend/
│   ├── models.py          # Database models (User, Item, Loan, Fine)
│   ├── database.py        # Database engine + session setup
│   ├── repository.py      # CRUD operations and business logic
│   ├── security.py        # Password hashing & authentication
│   └── init_db.py         # Creates tables and initializes the database
│
├── logic/
│   ├── checkout.py        # Checkout workflows
│   ├── returns.py         # Return workflows
│   ├── fines.py           # Fine tracking
│   └── overdue.py         # Overdue loan detection
│
├── gui/
│   ├── login_dialog.py    # Login screen
│   ├── main_window.py     # Main application interface
│   ├── return_window.py   # Return management (optional)
│   └── fines_window.py    # Fine management UI (optional)
│
├── tests/
│   └── test_backend.py    # Functional testing for repository layer
│
└── README.md

---

## ⚙️ Tools & Technologies
| Component | Technology |
|------------|-------------|
| **Language** | Python |
| **Database** | SQLite with SQLAlchemy ORM |
| **GUI Framework** | PySide6 |
| **Scheduler** | APScheduler |
| **Build Tool** | PyInstaller |
| **Version Control** | Git & GitHub |

---
🪄 How to Run(Using Bash)

# Clone the repository
git clone https://github.com/Ebun-25/Lendwise.git
cd Lendwise

# Create virtual environment
python -m venv venv
source venv/Scripts/activate  # On Windows

# Install dependencies
pip install -r requirements.txt

# Initialize database
python -m backend.init_db

# Run the app
python -m gui.main_window



