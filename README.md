
**SPARE MANAGER**

Inventory Management System

_README & Project Documentation_

Version 1.0 | 9 May 2026

**1\. Project Overview**

Spare Manager is a lightweight, offline-first inventory and spares management system built for small maintenance/engineering teams. It runs entirely on a local machine with no internet connection required, making it suitable for workshop and industrial environments.

The system tracks two types of inventory items:

- Reusable Spares - items like compressors and spanners that are borrowed and must be returned
- Consumables - items like globes, tape, and wire that are issued out and may or may not be returned

Key goals of this system:

- Maintain accurate stock levels at all times
- Track who did what and when - full audit trail for accountability
- Alert the General Manager via email when stock falls below threshold
- Back up the database automatically and email it offsite in case of system failure
- Package as a standalone executable - no Python installation required on the target machine

**2\. Technology Stack**

| **Layer**               | **Technology**           | **Reason**                                                            |
| ----------------------- | ------------------------ | --------------------------------------------------------------------- |
| Backend / Framework     | Flask (Python)           | Lightweight, no API layer needed, renders HTML directly               |
| Templating              | Jinja2                   | Built into Flask, server-side HTML rendering                          |
| Database                | SQLite                   | File-based, zero setup, perfect for offline use                       |
| Styling                 | Custom CSS               | Full control, no Bootstrap dependency, dark theme with orange accents |
| Email (alerts + backup) | smtplib + email (stdlib) | Built into Python, no third-party service needed                      |
| Backup                  | shutil (stdlib)          | Built into Python, copies DB file with timestamp                      |
| Packaging               | PyInstaller              | Bundles entire app into a single .exe for distribution                |
| Scheduling              | schedule (pip)           | Triggers daily backup + email automatically                           |

**3\. Features**

**3.1 Authentication & Role-Based Access**

Every user must log in before accessing the system. Three roles are supported:

| **Role**        | **Can Add/Edit/Delete Items** | **View Audit Log** | **App Settings & Users** | **Receives Email Alerts** |
| --------------- | ----------------------------- | ------------------ | ------------------------ | ------------------------- |
| Admin           | No                            | Yes                | Yes                      | No                        |
| Store Manager   | Yes                           | No                 | No                       | No                        |
| General Manager | Yes                           | Yes                | No                       | Yes                       |

**3.2 Inventory Management (Manage Spares)**

- Add new spares with name, spare code, initial quantity, low stock threshold, location/notes, and optional image
- View all spares in a searchable table (search by name or code)
- Edit spare details by double-clicking a row
- Delete spares (Store Manager and General Manager only)
- Stock status automatically calculated: In Stock / Low Stock / Out of Stock

**3.3 Borrow Items**

- Select a spare from the inventory dropdown
- Enter quantity to borrow, borrower name, and purpose/notes
- System deducts borrowed quantity from available stock
- Borrowed items appear in the Return Items list until returned

**3.4 Return Items**

- View all currently borrowed items with outstanding quantities
- Process full or partial returns
- Returned quantities are added back to inventory
- Surplus consumables can be returned even if item type is consumable

**3.5 Reports & Audit Log**

- Full audit trail: every add, edit, delete, borrow, and return is logged
  - Who performed the action (username + role)
  - Which item was affected
  - Previous value → New value
  - Timestamp
- Low stock report: all items currently below threshold
- Borrow/return history with date filters
- Audit log visible to Admin and General Manager only

**3.6 Alerts**

- When stock falls below the configured threshold, the system automatically emails the General Manager
- Email includes item name, code, current quantity, and threshold
- Alerts are triggered on every inventory update that results in low stock

**3.7 Database Backup**

- On every app startup, the database is backed up with a timestamp
- Daily scheduled backup runs automatically in the background
- Backup file (.db) is emailed as an attachment to the General Manager
- Provides offsite protection in case of hardware failure or app crash

**4\. Database Schema**

**users**

| **Column**    | **Type**   | **Description**                           |
| ------------- | ---------- | ----------------------------------------- |
| id            | INTEGER PK | Auto-increment primary key                |
| username      | TEXT       | Login username (unique)                   |
| password_hash | TEXT       | Hashed password                           |
| role          | TEXT       | admin \| store_manager \| general_manager |
| created_at    | DATETIME   | Account creation timestamp                |

**spares**

| **Column**     | **Type**   | **Description**                |
| -------------- | ---------- | ------------------------------ |
| id             | INTEGER PK | Auto-increment primary key     |
| name           | TEXT       | Spare name                     |
| code           | TEXT       | Spare code (unique identifier) |
| quantity       | INTEGER    | Current available quantity     |
| threshold      | INTEGER    | Low stock alert threshold      |
| location_notes | TEXT       | Storage location or notes      |
| image_path     | TEXT       | Optional path to spare image   |
| item_type      | TEXT       | reusable \| consumable         |
| created_at     | DATETIME   | Record creation timestamp      |

**borrow_records**

| **Column**        | **Type**   | **Description**                     |
| ----------------- | ---------- | ----------------------------------- |
| id                | INTEGER PK | Auto-increment primary key          |
| spare_id          | INTEGER FK | References spares.id                |
| borrowed_by       | TEXT       | Name of borrower                    |
| quantity_borrowed | INTEGER    | Amount taken from stock             |
| quantity_returned | INTEGER    | Amount returned so far (default 0)  |
| purpose           | TEXT       | Reason for borrowing                |
| borrowed_at       | DATETIME   | Date/time of borrow                 |
| returned_at       | DATETIME   | Date/time of full return (nullable) |
| user_id           | INTEGER FK | User who processed the transaction  |

**audit_log**

| **Column**     | **Type**   | **Description**                           |
| -------------- | ---------- | ----------------------------------------- |
| id             | INTEGER PK | Auto-increment primary key                |
| user_id        | INTEGER FK | Who performed the action                  |
| action         | TEXT       | add \| edit \| delete \| borrow \| return |
| item_name      | TEXT       | Name of the affected spare                |
| detail         | TEXT       | Human-readable description of change      |
| previous_value | TEXT       | State before change (nullable)            |
| new_value      | TEXT       | State after change (nullable)             |
| timestamp      | DATETIME   | When the action occurred                  |

**5\. Color Palette & Design System**

| **Role**              | **Color Name** | **Hex Code** | **Usage**                        |
| --------------------- | -------------- | ------------ | -------------------------------- |
| Background            | Deep Dark      | #0f0f0f      | Main app background              |
| Surface               | Dark Surface   | #1a1a1a      | Cards, sidebar, panels           |
| Border                | Subtle Dark    | #2a2a2a      | Dividers, input borders          |
| Primary Accent        | Orange         | #F97316      | Buttons, active nav, logo, links |
| Text Primary          | White          | #FFFFFF      | Main readable text               |
| Text Secondary        | Muted Gray     | #888888      | Labels, secondary info           |
| Status: OK            | Green          | #22c55e      | In Stock status                  |
| Status: Warning       | Orange         | #F97316      | Low Stock status                 |
| Status: Critical      | Red            | #ef4444      | Out of Stock / danger actions    |
| Status: Borrowed      | Blue           | #3b82f6      | Borrowed/pending state           |
| Role: Admin           | Purple         | #6366f1      | Admin badge and avatar           |
| Role: Store Manager   | Orange         | #F97316      | Store Manager badge              |
| Role: General Manager | Blue           | #3b82f6      | General Manager badge            |

**6\. Project Structure**

spare_manager/ ├── app.py # Main Flask application ├── database.py # SQLite setup & queries ├── email_utils.py # smtplib email + backup logic ├── backup.py # Backup scheduling ├── config.py # App configuration (email, thresholds) ├── database.db # SQLite database file ├── requirements.txt # Python dependencies ├── spare_manager.spec # PyInstaller config ├── static/ │ ├── css/ │ │ └── style.css # Main stylesheet │ ├── js/ │ │ └── main.js # Minimal vanilla JS │ └── images/ # Spare item images └── templates/ ├── base.html # Base layout (sidebar + topbar) ├── login.html # Login page ├── dashboard.html # Dashboard with stats ├── manage_spares.html # View + search spares ├── add_spare.html # Add new spare form ├── borrow.html # Borrow items form ├── return.html # Return items table ├── reports.html # Reports + audit log └── settings.html # Admin: users + email config

**7\. Setup & Installation (Development)**

**Prerequisites**

- Python 3.10 or higher
- pip (Python package manager)
- A Gmail account with App Password enabled (for email features)

**Installation Steps**

- Clone or download the project folder
- Install dependencies:

pip install -r requirements.txt

- Configure email settings in config.py
- Run the app:

python app.py

- Open browser to: <http://localhost:5000>

**Building the Executable**

pyinstaller spare_manager.spec

The output .exe will be in the dist/ folder. Copy it along with the database.db file to the target machine. Double-click to run - no Python installation required.

**8\. Email Configuration**

The system uses Gmail SMTP with an App Password. To set this up:

- Go to your Google Account → Security → 2-Step Verification (enable it)
- Under 2-Step Verification, find App Passwords
- Create a new App Password for Mail
- Paste the generated password into config.py

Two types of automated emails are sent:

- Low Stock Alert - sent to General Manager when any item falls below its threshold
- Database Backup - sent on app startup and once daily as a .db file attachment

**9\. Security Notes**

- Passwords are stored as hashed values (werkzeug.security) - never plain text
- Flask sessions are used for login state - session expires on browser close
- Role checks are enforced on every route - not just in the UI
- The audit log cannot be deleted by any user role - it is append-only
- config.py containing email credentials should never be committed to version control

**10\. Known Limitations & Future Considerations**

- Single machine only - not designed for multiple concurrent users on a network
- No automatic app updates - new versions must be manually deployed
- Email requires an active internet connection at the time of sending
- Images stored locally - not in the database, so backup must include the images folder

Future enhancements (out of scope for v1.0):

- Multi-user network access
- PDF report generation
- Barcode/QR code scanning for spare codes
- Mobile-friendly responsive layout

_Built with Flask · SQLite · Python · Custom CSS | Offline-first · No cloud required_