# NEVO TECH — Full-Stack Interactive Platform & Admin Dashboard

Engineered with a high-performance **Dark Cyber** UI/UX design system (`Palette 03 - Graphite + Cyber Cyan + Emerald Green`), powered by a **Flask** backend with **Supabase PostgreSQL** cloud persistence and a full-featured **Admin Dashboard**.

---

## 🌟 Quick Start & Running Locally

### 1. Prerequisites
- Python 3.10+ installed

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Configuration
Copy `.env.example` to `.env` (or configure your own variables):
```bash
cp .env.example .env
```

Default `.env` configuration:
```ini
DATABASE_URL=[REDACTED DATABASE URL]
PORT=5000
SECRET_KEY=[REDACTED]
ADMIN_PASSWORD=[REDACTED]
FLASK_ENV=development
```

### 4. Run the Backend Server
```bash
python server.py
```
The server will start on **http://localhost:5000/** with direct connection to Supabase PostgreSQL.

---

## 🔐 Admin Dashboard

The Admin Dashboard provides real-time oversight of all student and corporate inquiries.

| Access Point | URL | Credentials / Notes |
| :--- | :--- | :--- |
| **Admin Portal** | [http://localhost:5000/admin](http://localhost:5000/admin) | Password: `admin123` |
| **Admin Login** | [http://localhost:5000/admin/login](http://localhost:5000/admin/login) | Protected Session Authentication |
| **CSV Export** | [http://localhost:5000/admin/export-csv](http://localhost:5000/admin/export-csv) | One-click lead export for CRM |
| **Public Site** | [http://localhost:5000/](http://localhost:5000/) | Live website with enquiry forms |

### Admin Features:
- **KPI Metrics**: Real-time counters for Total Inquiries, New Leads, In Progress, and Enrolled conversions.
- **Database Status Indicator**: Live pill displaying cloud database connectivity status.
- **Live Search & Multi-Filter**: Filter leads instantly by Program Track or Lead Status (`New`, `Contacted`, `In Progress`, `Enrolled`, `Closed`), and search by applicant name, email, or institution.
- **Inline Status Management**: Change candidate pipeline status via AJAX dropdown with instant UI feedback.
- **Quick-Actions**: Direct click-to-email (`mailto:`) and click-to-call (`tel:`) shortcuts.
- **Modal Lead Inspector**: View full details, academic institutions, focus domains, and client requirements.

---

## 📋 Service Tracks & Auto-Select Architecture

All consultation forms strictly require **zero amount / pricing options**, focusing purely on academic and technical alignment.

Whenever a visitor clicks on a specific service track, the system **automatically locks in the selected program** without presenting any dropdown options:

1. **Technical Internship Programs** (`service-technical-internships.html`)
   - Software engineering, AI/ML, and cloud systems with mentor code reviews.
2. **Business & Analytics Internship** (`service-business-analytics-internship.html`)
   - Applied training in BI dashboards, market audits, and data strategy.
3. **Customized Technical Projects & Documentation** (`service-custom-projects-documentation.html`)
   - Custom implementations with full source code, UML diagrams, and IEEE reports.
4. **Survey-Based Projects & Research Reports** (`service-survey-research-reports.html`)
   - Questionnaire design, statistical tabulations, and market research synthesis.

---

## 🔌 API Reference

### Submit Enquiry
- **Endpoint**: `POST /api/enquiries`
- **Access**: Public
- **Headers**: `Content-Type: application/json`
- **Request Body**:
```json
{
  "fullName": "Student Name",
  "email": "student@example.com",
  "phone": "+91 98765 43210",
  "service": "Technical Internship Programs",
  "institution": "PES University",
  "domain": "AI & Cloud DevOps",
  "message": "Interested in joining the upcoming cohort."
}
```
- **Response**: `201 Created`

### List Enquiries
- **Endpoint**: `GET /api/enquiries`
- **Access**: Admin session required
- **Query Params**: `service` (optional), `status` (optional)

### Update Lead Status
- **Endpoint**: `PATCH /api/enquiries/<id>`
- **Access**: Admin session required
- **Payload**: `{"status": "Contacted", "notes": "Called candidate"}`

---

## 🛠️ Project Structure

```
├── .env.example                               # Environment template
├── db.py                                      # Supabase Postgres + resilient fallback database layer
├── server.py                                  # Flask application server & API routes
├── requirements.txt                           # Python dependencies
├── app.js                                     # Frontend interactions, auto-select logic & API integration
├── styles.css                                 # Cyber Dark theme stylesheet
├── index.html                                 # Main landing page
├── service-technical-internships.html         # Technical Internship Track
├── service-business-analytics-internship.html # Business Analytics Track
├── service-custom-projects-documentation.html # Custom Projects Track
├── service-survey-research-reports.html       # Survey Research Track
├── templates/
│   ├── admin.html                             # Admin Dashboard UI
│   └── admin_login.html                       # Admin Login portal
└── assets/                                    # Logos, SVGs, and brand media
```

---

## 🌐 Production Deployment Guide

Deploy easily on **Render**, **Railway**, **Fly.io**, or any cloud VPS:
1. Connect your GitHub repository: `https://github.com/Hemanth2006-nov/Nevo-tech.git`
2. Set Environment Variables:
   - `DATABASE_URL`: Your Supabase connection string.
   - `ADMIN_PASSWORD`: Your custom admin password.
   - `SECRET_KEY`: A random secure key.
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `python server.py` (or `gunicorn server:app`)
