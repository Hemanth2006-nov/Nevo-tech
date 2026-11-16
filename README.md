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
Copy `.env.example` to `.env` and add your own credentials:
```powershell
Copy-Item .env.example .env
```

Configure these values in `.env` for local development:
```ini
APP_ENV=development
DATABASE_URL=your-supabase-postgresql-connection-string?sslmode=require
PORT=5000
SECRET_KEY=generate-a-unique-random-value
ADMIN_PASSWORD=use-a-unique-local-admin-password
```

For local development, `DATABASE_URL` may be left blank to use a local SQLite database. Production requires Supabase/PostgreSQL and does not fall back to SQLite.

### 4. Run the Backend Server
```bash
python server.py
```
The server will start on **http://localhost:5000/**.

---

## 🔐 Admin Dashboard

The Admin Dashboard provides real-time oversight of all student and corporate inquiries.

| Access Point | URL | Credentials / Notes |
| :--- | :--- | :--- |
| **Admin Portal** | [http://localhost:5000/admin](http://localhost:5000/admin) | Use the locally configured admin password |
| **Admin Login** | [http://localhost:5000/admin/login](http://localhost:5000/admin/login) | Protected Session Authentication |
| **CSV Export** | Admin dashboard | CSRF-protected one-click lead export for CRM |
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
- **Production verification**: Include the `captchaToken` returned by Cloudflare Turnstile when Turnstile is enabled.
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
- **CSRF**: Send the dashboard token in the `X-CSRFToken` header.
- **Payload**: `{"status": "Contacted", "notes": "Called candidate"}`

---

## 🛠️ Project Structure

```
├── .env.example                               # Environment template
├── db.py                                      # Supabase Postgres with development-only SQLite fallback
├── server.py                                  # Flask application server & API routes
├── requirements.txt                           # Python dependencies
├── render.yaml                                # Render web service deployment blueprint
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

The Flask service and Supabase database are separate services. A Render blueprint is included:

1. Rotate the Supabase database password before deployment. The old connection credential was present in the repository; removing it from current files cannot remove it from Git history.
2. In Supabase, use the PostgreSQL connection string from **Connect** (direct or session pooler) and keep SSL enabled. Set it as `DATABASE_URL` in the hosting provider; do not put it in source control.
3. Deploy the repository to Render using `render.yaml`. The blueprint uses `gunicorn`, enables forwarded-proxy handling for Render, and probes `/health/ready`.
4. Configure the required environment variables in Render:
   - `DATABASE_URL`: Rotated Supabase PostgreSQL connection string with `sslmode=require`.
   - `SECRET_KEY`: Generate with `python -c "import secrets; print(secrets.token_urlsafe(48))"`.
   - `ADMIN_PASSWORD_HASH`: Generate locally using `python -c "from getpass import getpass; from werkzeug.security import generate_password_hash; print(generate_password_hash(getpass()))"`. Store the hash, not the password.
   - `TURNSTILE_SITE_KEY` and `TURNSTILE_SECRET_KEY`: Create a Cloudflare Turnstile widget for the production hostname. `TURNSTILE_REQUIRED=true` is set in the blueprint.
   - Lead notifications: configure either SMTP (`SMTP_HOST`, `SMTP_FROM`, `NOTIFICATION_EMAIL_TO`, plus provider credentials as needed) or an HTTPS `LEAD_WEBHOOK_URL`.
5. After deploy, test the site, a real enquiry, admin login, lead notification, CSV export, and `/health/ready`. Check Render logs for DB/SMTP/webhook errors.

The blueprint runs a single Gunicorn worker so its default in-memory rate limiter is shared across request threads. Before adding workers or instances, provision Redis and set `RATELIMIT_STORAGE_URI` to its private Redis URL. Never expose a Redis URL publicly.

For Railway, Fly.io, or a VPS, use the same environment variables and run `gunicorn server:app --workers 1 --threads 4 --timeout 30`. Set `TRUST_PROXY=true` only when requests pass through exactly one trusted reverse proxy.

### Production safeguards and operations

- Public enquiries are rate-limited and validated server-side; configure Turnstile before opening the production site.
- Admin sign-in is rate-limited; admin changes and logout require CSRF tokens, sessions use secure cookie settings, and status/deletion/export/login events are recorded in `admin_audit_log`.
- `/health/live` checks that the web process is responsive. `/health/ready` also checks the database and is used by Render.
- Logs go to standard output and avoid logging enquiry contents. SMTP/webhook delivery failures are logged while the saved enquiry remains successful.
- The frontend does not keep enquiry PII in `localStorage`; it only shows confirmation after the backend confirms persistence.
- Add a privacy policy/consent notice that explains how enquiry contact details are used and retained. Configure Supabase backups and a retention process appropriate to your legal obligations.
- Replace any sample testimonials, client names, performance claims, and portfolio results with verifiable, permissioned material before publishing.
