# Spare Manager - Offline Inventory & Spares Management System

A comprehensive offline inventory management application for tracking spare parts, managing borrowing/returns, and maintaining audit logs. Built with Flask, SQLite, and a dark-themed responsive UI.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [System Architecture](#system-architecture)
- [Tech Stack](#tech-stack)
- [Installation & Setup](#installation--setup)
- [Configuration](#configuration)
- [User Roles & Permissions](#user-roles--permissions)
- [Database Schema](#database-schema)
- [Features Guide](#features-guide)
- [Building the Executable](#building-the-executable)
- [Project Structure](#project-structure)
- [Development](#development)

## 🎯 Overview

Spare Manager is an offline-first inventory management system designed for organizations that need to track spare parts, manage equipment borrowing, and maintain complete audit trails. The system operates entirely locally with optional email integration for backup notifications and alerts.

**Key Characteristics:**
- 💻 Fully offline operation (no internet required)
- 📊 Real-time inventory tracking
- 🔄 Borrow/Return management with condition tracking
- 📝 Append-only audit logs for compliance
- 🎨 Dark theme optimized UI
- 📧 Optional email alerts and backups
- 🔐 Role-based access control
- 💾 SQLite database (portable, no server needed)

## ✨ Features

### Core Inventory Management
- **Add Spares**: Create new spare items with part numbers, descriptions, and locations
- **Categorize Items**: Define items as reusable (must be returned) or consumable (may be returned)
- **Track Quantities**: Monitor stock levels with automatic low-stock warnings
- **Search & Filter**: Quick lookup by name, part number, or item type
- **Edit/Delete**: Modify spare information or remove items

### Borrow & Return System
- **Borrow Requests**: Users can request items with purpose and expected return date
- **Automatic Deduction**: Quantity automatically decreases on borrow
- **Condition Tracking**: Record condition of returned items (good, damaged, etc.)
- **Flexible Returns**: Support partial returns for consumables
- **Borrow History**: Track all borrow/return transactions

### Reporting & Audit
- **Audit Log**: Append-only transaction log of all system actions
- **Inventory Reports**: Real-time inventory status and low-stock alerts
- **User Actions**: Track who performed each action and when
- **Compliance Ready**: Immutable audit trail for regulatory compliance

### System Features
- **User Management**: Create accounts with role-based permissions
- **Database Backup**: Automatic daily backups with email delivery
- **Email Alerts**: Notifications for low stock and return reminders
- **Session Management**: Secure session handling with timeout
- **Responsive UI**: Works on desktop and tablet browsers

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────┐
│                  Web Browser (Jinja2)               │
│              Dark Theme UI (#0f0f0f, #F97316)       │
└──────────────┬──────────────────────────────────────┘
               │
┌──────────────▼──────────────────────────────────────┐
│                    Flask Application                │
│  ┌────────────────────────────────────────────────┐ │
│  │  Routes: Auth, Spares, Borrow, Return, Reports│ │
│  └────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────┐ │
│  │  Middleware: Auth, Role-Based Access, Audit   │ │
│  └────────────────────────────────────────────────┘ │
└──────────────┬──────────────────────────────────────┘
               │
┌──────────────▼──────────────────────────────────────┐
│             Business Logic Layer                     │
│  ┌────────────────────────────────────────────────┐ │
│  │  Database Models (SQLAlchemy)                  │ │
│  │  Auth & Permissions                            │ │
│  │  Email Service (smtplib)                       │ │
│  │  Backup Management                             │ │
│  │  Background Scheduler (schedule)               │ │
│  └────────────────────────────────────────────────┘ │
└──────────────┬──────────────────────────────────────┘
               │
┌──────────────▼──────────────────────────────────────┐
│          SQLite Database (spare_manager.db)         │
│  ┌────────────────────────────────────────────────┐ │
│  │ Tables: Users, Spares, Borrows, Returns, Logs │ │
│  └────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────┘
```

## 🛠 Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | HTML5, CSS3, JavaScript | User interface |
| **Backend** | Flask 3.0 | Web framework |
| **Templating** | Jinja2 | Dynamic HTML rendering |
| **Database** | SQLite | Lightweight, portable data storage |
| **ORM** | SQLAlchemy 2.0 | Database abstraction |
| **Email** | smtplib | Backup and alert delivery |
| **Scheduling** | schedule | Recurring tasks (backups, cleanup) |
| **Packaging** | PyInstaller | Executable distribution |
| **Theme** | Custom CSS | Dark mode with orange accent (#F97316) |

## 📦 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Windows 10+ or macOS/Linux

### Step 1: Clone or Download Project
```bash
cd Alin-Elfen-Spare-Management-app
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Initialize Database
```bash
python -c "from app import create_app; app = create_app(); app.app_context().push()"
```

This creates the SQLite database and default admin user:
- **Username:** admin
- **Password:** admin123

⚠️ **Change this password immediately in Settings after first login!**

### Step 5: Configure Environment (Optional)
Create a `.env` file in the project root for custom settings:

```env
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_SENDER=your-email@gmail.com
BACKUP_RECIPIENTS=admin@company.com,manager@company.com
BACKUP_ENABLED=true
```

### Step 6: Run Application
```bash
python app.py
```

Application starts on `http://127.0.0.1:5000`

## ⚙️ Configuration

### Email Setup

To enable email backups and alerts, configure SMTP in `.env`:

```env
# Gmail Example (requires App Password)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_SENDER=your-email@gmail.com

# Local SMTP (Postfix, etc.)
SMTP_SERVER=localhost
SMTP_PORT=25
SMTP_SENDER=spare-manager@local.domain
```

**For Gmail:**
1. Enable 2-Factor Authentication
2. Generate App Password: https://myaccount.google.com/apppasswords
3. Use App Password in configuration

### Backup Settings

```env
# Enable/disable daily backups
BACKUP_ENABLED=true

# Recipients for backup emails (comma-separated)
BACKUP_RECIPIENTS=admin@company.com,backup@company.com
```

**Backup Schedule:**
- **Daily Backup:** 2:00 AM
- **Cleanup:** Every Sunday at 3:00 AM (removes backups older than 7 days)
- **Startup Backup:** Triggered on application start

### Database Location

Default: `spare_manager.db` (project root)

To change location, modify in `config.py`:
```python
SQLALCHEMY_DATABASE_URI = 'sqlite:////path/to/spare_manager.db'
```

## 👥 User Roles & Permissions

### Role Hierarchy

| Action | Admin | Store Manager | General Manager |
|--------|:-----:|:-------------:|:---------------:|
| View Dashboard | ✅ | ✅ | ✅ |
| View Spares | ✅ | ✅ | ✅ |
| Add/Edit/Delete Spares | ❌ | ✅ | ✅ |
| Borrow Items | ✅ | ✅ | ✅ |
| Return Items | ✅ | ✅ | ✅ |
| View Audit Log | ✅ | ❌ | ✅ |
| View Reports | ✅ | ❌ | ✅ |
| Manage Users | ✅ | ❌ | ❌ |
| Settings | ✅ | ❌ | ❌ |

### Admin
- Full system access
- User account management
- System settings and configuration
- View audit logs for compliance
- Cannot directly modify spares (intended design: admins manage users, not inventory)

### Store Manager
- Full inventory management (add, edit, delete spares)
- Borrow and return operations
- Inventory reports and search
- No access to audit logs or user management

### General Manager
- Same inventory access as Store Manager
- **Plus:** Access to audit logs for review
- Receives automated email alerts (backups, low stock warnings)
- Compliance reporting capability

## 📊 Database Schema

### users
```sql
id              INTEGER PRIMARY KEY
username        VARCHAR(80) UNIQUE NOT NULL
password_hash   VARCHAR(255) NOT NULL
email           VARCHAR(120)
role            VARCHAR(20) -- 'admin', 'store_manager', 'general_manager'
created_at      DATETIME
updated_at      DATETIME
is_active       BOOLEAN
```

### spares
```sql
id                INTEGER PRIMARY KEY
name              VARCHAR(120) NOT NULL
description       TEXT
item_type         VARCHAR(20) -- 'reusable', 'consumable'
quantity_in_stock INTEGER
minimum_quantity  INTEGER
unit              VARCHAR(50) -- 'pcs', 'box', 'set'
location          VARCHAR(200)
part_number       VARCHAR(120) UNIQUE
created_at        DATETIME
updated_at        DATETIME
created_by_id     INTEGER FOREIGN KEY
```

### borrow_records
```sql
id                     INTEGER PRIMARY KEY
spare_id               INTEGER FOREIGN KEY
quantity               INTEGER
borrowed_by_id         INTEGER FOREIGN KEY
purpose                TEXT
expected_return_date   DATETIME
borrowed_at            DATETIME
returned_at            DATETIME
is_returned            BOOLEAN
```

### return_records
```sql
id                  INTEGER PRIMARY KEY
borrow_record_id    INTEGER FOREIGN KEY
quantity_returned   INTEGER
condition           VARCHAR(50) -- 'good', 'damaged', etc.
notes               TEXT
returned_by_id      INTEGER FOREIGN KEY
returned_at         DATETIME
```

### audit_logs (Append-Only)
```sql
id              INTEGER PRIMARY KEY
action          VARCHAR(50) -- 'create', 'update', 'delete', 'borrow', 'return'
entity_type     VARCHAR(50) -- 'spare', 'borrow_record', 'user'
entity_id       INTEGER
changes         TEXT -- JSON format
performed_by_id INTEGER FOREIGN KEY
timestamp       DATETIME INDEX
ip_address      VARCHAR(50)
```

## 🎮 Features Guide

### Dashboard
- **Overview Statistics:**
  - Total spares in inventory
  - Number of low-stock items
  - Active borrow requests
  - Current user role
- **Quick Actions:** Direct links to main features

### Spare Management
**List View:**
- Search by name or part number
- Filter by item type (reusable/consumable)
- View quantity, minimum level, and status
- Pagination for large inventories

**Add/Edit:**
- Spare name and part number
- Type: Reusable (must return) vs Consumable (may return)
- Initial/current quantity
- Minimum stock level for alerts
- Storage location for tracking
- Description and notes

### Borrow System
**Request Item:**
1. Select spare from available items
2. Specify quantity
3. Add purpose/reason
4. Set expected return date (optional)
5. System automatically deducts from stock

**View Borrow Records:**
- Filter by status (Active/Returned/All)
- See who borrowed, when, and expected return
- Quick action to return item

### Return System
**Return Item:**
1. Select active borrow record
2. Specify quantity returned (supports partial returns)
3. Note condition (good, damaged, etc.)
4. Add return notes
5. System automatically adds back to stock

**Return Tracking:**
- Full history of all returns
- Condition notes for damaged items
- Restore stock based on item type

### Reports
**Inventory Report:**
- Current stock levels for all items
- Low-stock warnings (items below minimum level)
- Location and part number reference

**Audit Log** (Admin/General Manager only):
- Chronological record of all system actions
- Filter by entity type
- User who performed action, timestamp, and IP
- Immutable record for compliance

### Settings (Admin Only)
**User Management:**
- Create new user accounts
- Assign roles (Admin, Store Manager, General Manager)
- Deactivate/reactivate users
- Email configuration

## 🔨 Building the Executable

### Prerequisites
```bash
pip install PyInstaller
```

### Build Single Executable
```bash
pyinstaller --onefile --windowed --name "SpareManager" \
  --add-data "templates:templates" \
  --add-data "static:static" \
  --icon=icon.ico \
  app.py
```

**Result:** `dist/SpareManager.exe`

### Build with Console
For debugging, include console window:
```bash
pyinstaller --oneconsole --windowed --name "SpareManager" \
  --add-data "templates:templates" \
  --add-data "static:static" \
  app.py
```

### Distribution
```
SpareManager-v1.0/
├── SpareManager.exe           # Executable
├── spare_manager.db           # Auto-created on first run
├── backups/                   # Auto-created for backups
└── README.txt                 # Instructions
```

## 📁 Project Structure

```
Alin-Elfen-Spare-Management-app/
├── app.py                     # Flask application factory
├── config.py                  # Configuration settings
├── database.py                # SQLAlchemy models
├── auth.py                    # Authentication & permissions
├── routes.py                  # All route handlers
├── backup.py                  # Database backup logic
├── email_service.py           # Email sending utilities
├── scheduler.py               # Background task scheduling
├── requirements.txt           # Python dependencies
├── .env                       # Configuration (create locally)
│
├── templates/                 # HTML templates
│   ├── base.html              # Base template with nav
│   ├── login.html             # Login form
│   ├── dashboard.html         # Dashboard overview
│   ├── spares/
│   │   ├── list.html          # View all spares
│   │   ├── add.html           # Add new spare
│   │   └── edit.html          # Edit spare
│   ├── borrow/
│   │   ├── list.html          # View borrow records
│   │   └── borrow.html        # Borrow item form
│   ├── return/
│   │   ├── list.html          # View returns
│   │   └── return.html        # Return item form
│   ├── reports/
│   │   ├── audit_log.html     # Audit log viewer
│   │   └── inventory.html     # Inventory report
│   └── settings/
│       └── index.html         # User & system settings
│
├── static/
│   ├── css/
│   │   └── style.css          # Dark theme styling
│   └── js/
│       └── app.js             # Frontend utilities
│
└── README.md                  # This file
```

## 🔒 Security Considerations

### Authentication
- Passwords hashed with werkzeug.security (PBKDF2)
- Session-based authentication with secure cookies
- 8-hour session timeout

### Authorization
- Role-based access control (RBAC)
- Decorator-based permission checking
- Route-level protection

### Audit Trail
- Append-only audit log (cannot be modified)
- Tracks user, timestamp, IP address, and changes
- Suitable for compliance requirements

### Database
- SQLite stored in project directory
- Can be backed up and encrypted externally
- Backup stored separately from main database

### Recommendations
1. **Change default admin password immediately**
2. **Use strong SMTP credentials for email**
3. **Backup database regularly** (automated via email)
4. **Monitor audit logs** for suspicious activity
5. **Use on trusted network only** (no external access)

## 🚀 Development

### Running in Development Mode
```bash
export FLASK_ENV=development
export FLASK_DEBUG=1
python app.py
```

Debug toolbar and auto-reload enabled.

### Adding New Routes
1. Create blueprint in `routes.py`
2. Define route functions with appropriate decorators
3. Create template in `templates/`
4. Register blueprint in `app.py`

### Database Migrations
For changes to models:
1. Update model in `database.py`
2. Delete existing `spare_manager.db`
3. Restart app to recreate with new schema

### Testing Locally
1. Create test users in Settings
2. Test each role's permissions
3. Verify borrow/return flow
4. Check audit log entries

### Performance Notes
- SQLite handles ~10,000 spares and 100,000 transactions efficiently
- Pagination at 20 items per page for UI responsiveness
- Indexing on timestamp for audit log queries
- Consider upgrading to PostgreSQL for larger deployments (1M+ records)

## 📝 License

Internal Use Only - Alin Elfen Organization

## 📧 Support

For issues or feature requests, document in:
- Audit log with reproduction steps
- Screenshots of error state
- Affected user accounts

---

**Version:** 1.0  
**Last Updated:** 2026-05-09  
**Status:** Ready for Development
