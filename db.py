import os
import sqlite3
import datetime
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)
APP_ENV = os.environ.get("APP_ENV", "development").lower()


def normalize_database_url(url):
    if not url:
        return None
    if "sslmode=" not in url:
        separator = "&" if "?" in url else "?"
        return f"{url}{separator}sslmode=require"
    return url


DATABASE_URL = normalize_database_url(os.environ.get("DATABASE_URL"))

IS_POSTGRES = False
DB_STATUS = "Local SQLite (development)"
if DATABASE_URL:
    import psycopg2
    from psycopg2.extras import RealDictCursor
    try:
        test_conn = psycopg2.connect(DATABASE_URL, connect_timeout=5, sslmode="require")
        test_conn.close()
        IS_POSTGRES = True
        DB_STATUS = "Connected to Supabase PostgreSQL"
        logger.info("Connected to Supabase PostgreSQL")
    except psycopg2.Error:
        if APP_ENV == "production":
            logger.exception("Could not connect to the configured PostgreSQL database")
            raise
        logger.exception("Supabase connection failed; using local SQLite for development")
elif APP_ENV == "production":
    raise RuntimeError("DATABASE_URL is required in production")

SQLITE_PATH = os.path.join(os.path.dirname(__file__), "nevo_database.db")


def get_db():
    if IS_POSTGRES:
        conn = psycopg2.connect(DATABASE_URL, connect_timeout=10, sslmode="require")
        return conn
    else:
        conn = sqlite3.connect(SQLITE_PATH)
        conn.row_factory = sqlite3.Row
        return conn


DEFAULT_TEAM_MEMBERS = [
    {
        "name": "Dr. Rajesh Kumar",
        "role": "Head of AI & Cloud Systems",
        "department": "Technical Internship Track",
        "photo_url": "/assets/mentor-rajesh.svg",
        "bio": "Ex-IISc research scholar with 12+ years specializing in distributed microservices, PyTorch neural models, and container orchestration.",
        "email": "rajesh.k@nevotech.in",
        "linkedin_url": "https://linkedin.com",
        "display_order": 1,
        "is_active": 1,
    },
    {
        "name": "Ananya Sharma",
        "role": "Director of Business Analytics & Insights",
        "department": "Business & Analytics Track",
        "photo_url": "/assets/mentor-ananya.svg",
        "bio": "Specializes in enterprise customer churn predictive models, PowerBI executive suites, and SQL financial cohort analysis.",
        "email": "ananya.s@nevotech.in",
        "linkedin_url": "https://linkedin.com",
        "display_order": 2,
        "is_active": 1,
    },
    {
        "name": "Vikramaditya Roy",
        "role": "Chief Technical Project Architect",
        "department": "Custom Technical Projects",
        "photo_url": "/assets/mentor-vikram.svg",
        "bio": "Oversees end-to-end IoT, embedded robotics, and full-stack systems with rigorous IEEE documentation standards.",
        "email": "vikram.r@nevotech.in",
        "linkedin_url": "https://linkedin.com",
        "display_order": 3,
        "is_active": 1,
    },
    {
        "name": "Sneha Patel",
        "role": "Lead Empirical Research Methodologist",
        "department": "Survey & Research Reports",
        "photo_url": "/assets/mentor-sneha.svg",
        "bio": "Expert in quantitative survey sampling, SPSS regression modeling, structural equation models, and academic manuscript publishing.",
        "email": "sneha.p@nevotech.in",
        "linkedin_url": "https://linkedin.com",
        "display_order": 4,
        "is_active": 1,
    },
]

DEFAULT_WEBSITE_ITEMS = [
    {
        "title": "Embedded IoT & Robotics Prototyping Lab",
        "category": "Lab & Campus",
        "description": "State-of-the-art hardware development benches equipped with oscilloscope rigs, FPGA boards, ESP32 arrays, and automated testing fixtures.",
        "photo_url": "/assets/office-render.svg",
        "badge_text": "HARDWARE LAB",
        "link_url": "#projects",
        "display_order": 1,
        "is_active": 1,
    },
    {
        "title": "Cloud-Native Microservices & AI Capstone",
        "category": "Featured Project",
        "description": "Production-grade distributed API with Docker containerization, Kubernetes manifests, and automated CI/CD pipelines delivered by engineering interns.",
        "photo_url": "/assets/project-devsync.svg",
        "badge_text": "PRODUCTION GRADE",
        "link_url": "#projects",
        "display_order": 2,
        "is_active": 1,
    },
    {
        "title": "Executive Customer Intelligence Engine",
        "category": "Analytics Showcase",
        "description": "Interactive PowerBI and Python executive dashboards incorporating customer churn predictive modeling and SQL cohort analytics.",
        "photo_url": "/assets/project-heavymachinery.svg",
        "badge_text": "DATA ANALYTICS",
        "link_url": "#projects",
        "display_order": 3,
        "is_active": 1,
    },
    {
        "title": "FinTech Adoption & Consumer Sentiment Study",
        "category": "Research Publication",
        "description": "Empirical quantitative paper based on 1,200+ survey responses with Cronbach's alpha verification, SPSS regression modeling, and academic manuscript.",
        "photo_url": "/assets/project-collegeportal.svg",
        "badge_text": "IEEE RESEARCH",
        "link_url": "#projects",
        "display_order": 4,
        "is_active": 1,
    },
]


def init_db():
    conn = get_db()
    cur = conn.cursor()
    if IS_POSTGRES:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS enquiries (
                id SERIAL PRIMARY KEY,
                full_name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                phone VARCHAR(50) NOT NULL,
                service VARCHAR(255) NOT NULL,
                institution VARCHAR(255),
                domain VARCHAR(255),
                message TEXT,
                status VARCHAR(50) DEFAULT 'New',
                notes TEXT,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS admin_audit_log (
                id SERIAL PRIMARY KEY,
                actor VARCHAR(255) NOT NULL,
                action VARCHAR(50) NOT NULL,
                enquiry_id INTEGER,
                details TEXT,
                occurred_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS team_members (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                role VARCHAR(255) NOT NULL,
                department VARCHAR(255),
                photo_url TEXT,
                bio TEXT,
                email VARCHAR(255),
                linkedin_url TEXT,
                display_order INTEGER DEFAULT 0,
                is_active INTEGER DEFAULT 1,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS website_items (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                category VARCHAR(100) NOT NULL,
                description TEXT NOT NULL,
                photo_url TEXT NOT NULL,
                badge_text VARCHAR(100),
                link_url TEXT,
                display_order INTEGER DEFAULT 0,
                is_active INTEGER DEFAULT 1,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()

        # Seed default team members if empty
        cur.execute("SELECT COUNT(*) FROM team_members;")
        if cur.fetchone()[0] == 0:
            for m in DEFAULT_TEAM_MEMBERS:
                cur.execute("""
                    INSERT INTO team_members (name, role, department, photo_url, bio, email, linkedin_url, display_order, is_active)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (m["name"], m["role"], m["department"], m["photo_url"], m["bio"], m["email"], m["linkedin_url"], m["display_order"], m["is_active"]))
            conn.commit()

        # Seed default website items if empty
        cur.execute("SELECT COUNT(*) FROM website_items;")
        if cur.fetchone()[0] == 0:
            for item in DEFAULT_WEBSITE_ITEMS:
                cur.execute("""
                    INSERT INTO website_items (title, category, description, photo_url, badge_text, link_url, display_order, is_active)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (item["title"], item["category"], item["description"], item["photo_url"], item["badge_text"], item["link_url"], item["display_order"], item["is_active"]))
            conn.commit()

    else:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS enquiries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL,
                service TEXT NOT NULL,
                institution TEXT,
                domain TEXT,
                message TEXT,
                status TEXT DEFAULT 'New',
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS admin_audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                actor TEXT NOT NULL,
                action TEXT NOT NULL,
                enquiry_id INTEGER,
                details TEXT,
                occurred_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS team_members (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                role TEXT NOT NULL,
                department TEXT,
                photo_url TEXT,
                bio TEXT,
                email TEXT,
                linkedin_url TEXT,
                display_order INTEGER DEFAULT 0,
                is_active INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS website_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                category TEXT NOT NULL,
                description TEXT NOT NULL,
                photo_url TEXT NOT NULL,
                badge_text TEXT,
                link_url TEXT,
                display_order INTEGER DEFAULT 0,
                is_active INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()

        # Seed default team members if empty
        cur.execute("SELECT COUNT(*) FROM team_members;")
        if cur.fetchone()[0] == 0:
            for m in DEFAULT_TEAM_MEMBERS:
                cur.execute("""
                    INSERT INTO team_members (name, role, department, photo_url, bio, email, linkedin_url, display_order, is_active)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (m["name"], m["role"], m["department"], m["photo_url"], m["bio"], m["email"], m["linkedin_url"], m["display_order"], m["is_active"]))
            conn.commit()

        # Seed default website items if empty
        cur.execute("SELECT COUNT(*) FROM website_items;")
        if cur.fetchone()[0] == 0:
            for item in DEFAULT_WEBSITE_ITEMS:
                cur.execute("""
                    INSERT INTO website_items (title, category, description, photo_url, badge_text, link_url, display_order, is_active)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (item["title"], item["category"], item["description"], item["photo_url"], item["badge_text"], item["link_url"], item["display_order"], item["is_active"]))
            conn.commit()

    cur.close()
    conn.close()
    logger.info("Database schema initialized with team_members and website_items")


# ==============================================================================
# ENQUIRIES / LEADS OPERATIONS
# ==============================================================================

def insert_enquiry(data):
    conn = get_db()
    cur = conn.cursor()
    
    full_name = data.get("fullName", "").strip()
    email = data.get("email", "").strip()
    phone = data.get("phone", "").strip()
    service = data.get("service", "General Consultation").strip()
    institution = data.get("institution", "").strip()
    domain = data.get("domain", "").strip()
    message = data.get("message", "").strip()
    status = data.get("status", "New").strip()
    notes = data.get("notes", "").strip()
    
    if IS_POSTGRES:
        query = """
            INSERT INTO enquiries (full_name, email, phone, service, institution, domain, message, status, notes)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id, created_at;
        """
        cur.execute(query, (full_name, email, phone, service, institution, domain, message, status, notes))
        row = cur.fetchone()
        enquiry_id = row[0]
        created_at = row[1].isoformat() if hasattr(row[1], 'isoformat') else str(row[1])
    else:
        query = """
            INSERT INTO enquiries (full_name, email, phone, service, institution, domain, message, status, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
        """
        cur.execute(query, (full_name, email, phone, service, institution, domain, message, status, notes))
        enquiry_id = cur.lastrowid
        created_at = datetime.datetime.now().isoformat()

    _insert_audit(cur, "public", "enquiry_created", enquiry_id)
    conn.commit()
        
    cur.close()
    conn.close()
    return {"id": enquiry_id, "created_at": created_at}


def create_enquiry_by_admin(data):
    conn = get_db()
    cur = conn.cursor()
    
    full_name = data.get("fullName", "").strip()
    email = data.get("email", "").strip()
    phone = data.get("phone", "").strip()
    service = data.get("service", "Technical Internship Programs").strip()
    institution = data.get("institution", "").strip()
    domain = data.get("domain", "").strip()
    message = data.get("message", "").strip()
    status = data.get("status", "New").strip()
    notes = data.get("notes", "").strip()
    
    if IS_POSTGRES:
        query = """
            INSERT INTO enquiries (full_name, email, phone, service, institution, domain, message, status, notes)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id, created_at;
        """
        cur.execute(query, (full_name, email, phone, service, institution, domain, message, status, notes))
        row = cur.fetchone()
        enquiry_id = row[0]
        created_at = row[1].strftime("%b %d, %Y - %I:%M %p") if hasattr(row[1], 'strftime') else str(row[1])
    else:
        query = """
            INSERT INTO enquiries (full_name, email, phone, service, institution, domain, message, status, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
        """
        cur.execute(query, (full_name, email, phone, service, institution, domain, message, status, notes))
        enquiry_id = cur.lastrowid
        created_at = datetime.datetime.now().strftime("%b %d, %Y - %I:%M %p")

    _insert_audit(cur, "admin", "enquiry_created_admin", enquiry_id, f"Added person: {full_name}")
    conn.commit()
    cur.close()
    conn.close()
    return {
        "id": enquiry_id,
        "full_name": full_name,
        "email": email,
        "phone": phone,
        "service": service,
        "institution": institution,
        "domain": domain,
        "message": message,
        "status": status,
        "notes": notes,
        "created_at": created_at,
    }


def get_all_enquiries(service_filter=None, status_filter=None, search=None, category=None, track=None):
    conn = get_db()
    enquiries = []
    
    # Handle composite service_filter values if category/track not explicitly passed
    if service_filter:
        sf = service_filter.lower().strip()
        if sf == 'internship':
            category = 'internship'
        elif sf in ('projects', 'project'):
            category = 'projects'
        elif sf == 'tech':
            track = 'tech'
        elif sf in ('nontech', 'non-tech'):
            track = 'nontech'
        elif sf in ('internship_tech', 'internship-tech'):
            category = 'internship'
            track = 'tech'
        elif sf in ('internship_nontech', 'internship-nontech'):
            category = 'internship'
            track = 'nontech'
        elif sf in ('projects_tech', 'projects-tech'):
            category = 'projects'
            track = 'tech'
        elif sf in ('projects_nontech', 'projects-nontech'):
            category = 'projects'
            track = 'nontech'
        else:
            # exact service string filter
            pass

    if IS_POSTGRES:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        query = "SELECT * FROM enquiries WHERE 1=1"
        params = []
        
        if category == 'internship':
            query += " AND service ILIKE '%Internship%'"
        elif category == 'projects':
            query += " AND (service ILIKE '%Project%' OR service ILIKE '%Research%' OR service ILIKE '%Partnership%')"

        if track == 'tech':
            query += " AND service ILIKE '%Technical%'"
        elif track == 'nontech':
            query += " AND service NOT ILIKE '%Technical%'"

        # If an explicit service string that wasn't category/track shorthand
        if service_filter and not category and not track:
            query += " AND service = %s"
            params.append(service_filter)

        if status_filter:
            query += " AND status = %s"
            params.append(status_filter)
        if search:
            query += " AND (full_name ILIKE %s OR email ILIKE %s OR phone ILIKE %s OR institution ILIKE %s OR domain ILIKE %s)"
            s_param = f"%{search}%"
            params.extend([s_param, s_param, s_param, s_param, s_param])
            
        query += " ORDER BY id DESC"
        cur.execute(query, params)
        rows = cur.fetchall()
        for r in rows:
            d = dict(r)
            if "created_at" in d and d["created_at"]:
                d["created_at"] = d["created_at"].strftime("%b %d, %Y - %I:%M %p")
            enquiries.append(d)
        cur.close()
    else:
        cur = conn.cursor()
        query = "SELECT * FROM enquiries WHERE 1=1"
        params = []
        
        if category == 'internship':
            query += " AND service LIKE '%Internship%'"
        elif category == 'projects':
            query += " AND (service LIKE '%Project%' OR service LIKE '%Research%' OR service LIKE '%Partnership%')"

        if track == 'tech':
            query += " AND service LIKE '%Technical%'"
        elif track == 'nontech':
            query += " AND service NOT LIKE '%Technical%'"

        if service_filter and not category and not track:
            query += " AND service = ?"
            params.append(service_filter)

        if status_filter:
            query += " AND status = ?"
            params.append(status_filter)
        if search:
            query += " AND (full_name LIKE ? OR email LIKE ? OR phone LIKE ? OR institution LIKE ? OR domain LIKE ?)"
            s_param = f"%{search}%"
            params.extend([s_param, s_param, s_param, s_param, s_param])
            
        query += " ORDER BY id DESC"
        cur.execute(query, params)
        rows = cur.fetchall()
        for r in rows:
            d = dict(r)
            enquiries.append(d)
        cur.close()
        
    conn.close()
    return enquiries


def get_enquiry_by_id(enquiry_id):
    conn = get_db()
    res = None
    if IS_POSTGRES:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM enquiries WHERE id = %s", (enquiry_id,))
        row = cur.fetchone()
        if row:
            res = dict(row)
            if "created_at" in res and res["created_at"]:
                res["created_at"] = res["created_at"].strftime("%b %d, %Y - %I:%M %p")
        cur.close()
    else:
        cur = conn.cursor()
        cur.execute("SELECT * FROM enquiries WHERE id = ?", (enquiry_id,))
        row = cur.fetchone()
        if row:
            res = dict(row)
        cur.close()
    conn.close()
    return res


def update_enquiry(enquiry_id, data):
    conn = get_db()
    cur = conn.cursor()
    
    full_name = data.get("fullName", "").strip()
    email = data.get("email", "").strip()
    phone = data.get("phone", "").strip()
    service = data.get("service", "").strip()
    institution = data.get("institution", "").strip()
    domain = data.get("domain", "").strip()
    message = data.get("message", "").strip()
    status = data.get("status", "New").strip()
    notes = data.get("notes", "").strip()
    
    if IS_POSTGRES:
        query = """
            UPDATE enquiries
            SET full_name = %s, email = %s, phone = %s, service = %s,
                institution = %s, domain = %s, message = %s, status = %s, notes = %s
            WHERE id = %s
        """
        cur.execute(query, (full_name, email, phone, service, institution, domain, message, status, notes, enquiry_id))
    else:
        query = """
            UPDATE enquiries
            SET full_name = ?, email = ?, phone = ?, service = ?,
                institution = ?, domain = ?, message = ?, status = ?, notes = ?
            WHERE id = ?
        """
        cur.execute(query, (full_name, email, phone, service, institution, domain, message, status, notes, enquiry_id))
    
    changed = cur.rowcount > 0
    if changed:
        _insert_audit(cur, "admin", "enquiry_modified", enquiry_id, f"Updated lead {full_name}")
    conn.commit()
    cur.close()
    conn.close()
    return changed


def update_enquiry_status(enquiry_id, status, notes=None):
    conn = get_db()
    cur = conn.cursor()
    if IS_POSTGRES:
        if notes is not None:
            cur.execute("UPDATE enquiries SET status = %s, notes = %s WHERE id = %s", (status, notes, enquiry_id))
        else:
            cur.execute("UPDATE enquiries SET status = %s WHERE id = %s", (status, enquiry_id))
    else:
        if notes is not None:
            cur.execute("UPDATE enquiries SET status = ?, notes = ? WHERE id = ?", (status, notes, enquiry_id))
        else:
            cur.execute("UPDATE enquiries SET status = ? WHERE id = ?", (status, enquiry_id))
    changed = cur.rowcount > 0
    if changed:
        _insert_audit(cur, "admin", "status_updated", enquiry_id, status)
    conn.commit()
    cur.close()
    conn.close()
    return changed


def delete_enquiry(enquiry_id):
    conn = get_db()
    cur = conn.cursor()
    if IS_POSTGRES:
        cur.execute("DELETE FROM enquiries WHERE id = %s", (enquiry_id,))
    else:
        cur.execute("DELETE FROM enquiries WHERE id = ?", (enquiry_id,))
    deleted = cur.rowcount > 0
    if deleted:
        _insert_audit(cur, "admin", "enquiry_deleted", enquiry_id, None)
    conn.commit()
    cur.close()
    conn.close()
    return deleted


# ==============================================================================
# TEAM MEMBERS / PEOPLE OPERATIONS ("Adding new peoples")
# ==============================================================================

def get_all_team_members(active_only=False):
    conn = get_db()
    members = []
    condition = "WHERE is_active = 1" if active_only else ""
    order_clause = "ORDER BY display_order ASC, id ASC"
    
    if IS_POSTGRES:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(f"SELECT * FROM team_members {condition} {order_clause};")
        rows = cur.fetchall()
        for r in rows:
            d = dict(r)
            if "created_at" in d and d["created_at"]:
                d["created_at"] = d["created_at"].strftime("%b %d, %Y")
            members.append(d)
        cur.close()
    else:
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM team_members {condition} {order_clause};")
        rows = cur.fetchall()
        for r in rows:
            members.append(dict(r))
        cur.close()
    conn.close()
    return members


def get_team_member(member_id):
    conn = get_db()
    member = None
    if IS_POSTGRES:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM team_members WHERE id = %s", (member_id,))
        row = cur.fetchone()
        if row:
            member = dict(row)
        cur.close()
    else:
        cur = conn.cursor()
        cur.execute("SELECT * FROM team_members WHERE id = ?", (member_id,))
        row = cur.fetchone()
        if row:
            member = dict(row)
        cur.close()
    conn.close()
    return member


def insert_team_member(data):
    conn = get_db()
    cur = conn.cursor()
    
    name = str(data.get("name", "")).strip()
    role = str(data.get("role", "")).strip()
    department = str(data.get("department", "")).strip()
    photo_url = str(data.get("photo_url", "")).strip() or "/assets/mentor-rajesh.svg"
    bio = str(data.get("bio", "")).strip()
    email = str(data.get("email", "")).strip()
    linkedin_url = str(data.get("linkedin_url", "")).strip()
    display_order = int(data.get("display_order", 0) or 0)
    is_active = 1 if str(data.get("is_active", "1")).lower() in {"1", "true", "yes"} else 0
    
    if IS_POSTGRES:
        query = """
            INSERT INTO team_members (name, role, department, photo_url, bio, email, linkedin_url, display_order, is_active)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id, created_at;
        """
        cur.execute(query, (name, role, department, photo_url, bio, email, linkedin_url, display_order, is_active))
        row = cur.fetchone()
        member_id = row[0]
        created_at = row[1].strftime("%b %d, %Y") if hasattr(row[1], 'strftime') else str(row[1])
    else:
        query = """
            INSERT INTO team_members (name, role, department, photo_url, bio, email, linkedin_url, display_order, is_active)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
        """
        cur.execute(query, (name, role, department, photo_url, bio, email, linkedin_url, display_order, is_active))
        member_id = cur.lastrowid
        created_at = datetime.datetime.now().strftime("%b %d, %Y")

    _insert_audit(cur, "admin", "team_member_created", None, f"Created team member: {name}")
    conn.commit()
    cur.close()
    conn.close()
    return {
        "id": member_id,
        "name": name,
        "role": role,
        "department": department,
        "photo_url": photo_url,
        "bio": bio,
        "email": email,
        "linkedin_url": linkedin_url,
        "display_order": display_order,
        "is_active": is_active,
        "created_at": created_at,
    }


def update_team_member(member_id, data):
    conn = get_db()
    cur = conn.cursor()
    
    name = str(data.get("name", "")).strip()
    role = str(data.get("role", "")).strip()
    department = str(data.get("department", "")).strip()
    photo_url = str(data.get("photo_url", "")).strip() or "/assets/mentor-rajesh.svg"
    bio = str(data.get("bio", "")).strip()
    email = str(data.get("email", "")).strip()
    linkedin_url = str(data.get("linkedin_url", "")).strip()
    display_order = int(data.get("display_order", 0) or 0)
    is_active = 1 if str(data.get("is_active", "1")).lower() in {"1", "true", "yes"} else 0
    
    if IS_POSTGRES:
        query = """
            UPDATE team_members
            SET name = %s, role = %s, department = %s, photo_url = %s, bio = %s,
                email = %s, linkedin_url = %s, display_order = %s, is_active = %s
            WHERE id = %s
        """
        cur.execute(query, (name, role, department, photo_url, bio, email, linkedin_url, display_order, is_active, member_id))
    else:
        query = """
            UPDATE team_members
            SET name = ?, role = ?, department = ?, photo_url = ?, bio = ?,
                email = ?, linkedin_url = ?, display_order = ?, is_active = ?
            WHERE id = ?
        """
        cur.execute(query, (name, role, department, photo_url, bio, email, linkedin_url, display_order, is_active, member_id))
    
    changed = cur.rowcount > 0
    if changed:
        _insert_audit(cur, "admin", "team_member_updated", None, f"Updated team member #{member_id}: {name}")
    conn.commit()
    cur.close()
    conn.close()
    return changed


def delete_team_member(member_id):
    conn = get_db()
    cur = conn.cursor()
    if IS_POSTGRES:
        cur.execute("DELETE FROM team_members WHERE id = %s", (member_id,))
    else:
        cur.execute("DELETE FROM team_members WHERE id = ?", (member_id,))
    deleted = cur.rowcount > 0
    if deleted:
        _insert_audit(cur, "admin", "team_member_deleted", None, f"Deleted team member #{member_id}")
    conn.commit()
    cur.close()
    conn.close()
    return deleted


# ==============================================================================
# WEBSITE DETAILS & PHOTOS (Showcase / Content Items)
# ==============================================================================

def get_all_website_items(active_only=False):
    conn = get_db()
    items = []
    condition = "WHERE is_active = 1" if active_only else ""
    order_clause = "ORDER BY display_order ASC, id ASC"
    
    if IS_POSTGRES:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(f"SELECT * FROM website_items {condition} {order_clause};")
        rows = cur.fetchall()
        for r in rows:
            d = dict(r)
            if "created_at" in d and d["created_at"]:
                d["created_at"] = d["created_at"].strftime("%b %d, %Y")
            items.append(d)
        cur.close()
    else:
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM website_items {condition} {order_clause};")
        rows = cur.fetchall()
        for r in rows:
            items.append(dict(r))
        cur.close()
    conn.close()
    return items


def get_website_item(item_id):
    conn = get_db()
    item = None
    if IS_POSTGRES:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM website_items WHERE id = %s", (item_id,))
        row = cur.fetchone()
        if row:
            item = dict(row)
        cur.close()
    else:
        cur = conn.cursor()
        cur.execute("SELECT * FROM website_items WHERE id = ?", (item_id,))
        row = cur.fetchone()
        if row:
            item = dict(row)
        cur.close()
    conn.close()
    return item


def insert_website_item(data):
    conn = get_db()
    cur = conn.cursor()
    
    title = str(data.get("title", "")).strip()
    category = str(data.get("category", "")).strip() or "General Showcase"
    description = str(data.get("description", "")).strip()
    photo_url = str(data.get("photo_url", "")).strip() or "/assets/office-render.svg"
    badge_text = str(data.get("badge_text", "")).strip() or category.upper()
    link_url = str(data.get("link_url", "")).strip()
    display_order = int(data.get("display_order", 0) or 0)
    is_active = 1 if str(data.get("is_active", "1")).lower() in {"1", "true", "yes"} else 0
    
    if IS_POSTGRES:
        query = """
            INSERT INTO website_items (title, category, description, photo_url, badge_text, link_url, display_order, is_active)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id, created_at;
        """
        cur.execute(query, (title, category, description, photo_url, badge_text, link_url, display_order, is_active))
        row = cur.fetchone()
        item_id = row[0]
        created_at = row[1].strftime("%b %d, %Y") if hasattr(row[1], 'strftime') else str(row[1])
    else:
        query = """
            INSERT INTO website_items (title, category, description, photo_url, badge_text, link_url, display_order, is_active)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        """
        cur.execute(query, (title, category, description, photo_url, badge_text, link_url, display_order, is_active))
        item_id = cur.lastrowid
        created_at = datetime.datetime.now().strftime("%b %d, %Y")

    _insert_audit(cur, "admin", "website_item_created", None, f"Added website item: {title}")
    conn.commit()
    cur.close()
    conn.close()
    return {
        "id": item_id,
        "title": title,
        "category": category,
        "description": description,
        "photo_url": photo_url,
        "badge_text": badge_text,
        "link_url": link_url,
        "display_order": display_order,
        "is_active": is_active,
        "created_at": created_at,
    }


def update_website_item(item_id, data):
    conn = get_db()
    cur = conn.cursor()
    
    title = str(data.get("title", "")).strip()
    category = str(data.get("category", "")).strip() or "General Showcase"
    description = str(data.get("description", "")).strip()
    photo_url = str(data.get("photo_url", "")).strip() or "/assets/office-render.svg"
    badge_text = str(data.get("badge_text", "")).strip() or category.upper()
    link_url = str(data.get("link_url", "")).strip()
    display_order = int(data.get("display_order", 0) or 0)
    is_active = 1 if str(data.get("is_active", "1")).lower() in {"1", "true", "yes"} else 0
    
    if IS_POSTGRES:
        query = """
            UPDATE website_items
            SET title = %s, category = %s, description = %s, photo_url = %s,
                badge_text = %s, link_url = %s, display_order = %s, is_active = %s
            WHERE id = %s
        """
        cur.execute(query, (title, category, description, photo_url, badge_text, link_url, display_order, is_active, item_id))
    else:
        query = """
            UPDATE website_items
            SET title = ?, category = ?, description = ?, photo_url = ?,
                badge_text = ?, link_url = ?, display_order = ?, is_active = ?
            WHERE id = ?
        """
        cur.execute(query, (title, category, description, photo_url, badge_text, link_url, display_order, is_active, item_id))
    
    changed = cur.rowcount > 0
    if changed:
        _insert_audit(cur, "admin", "website_item_updated", None, f"Updated website item #{item_id}: {title}")
    conn.commit()
    cur.close()
    conn.close()
    return changed


def delete_website_item(item_id):
    conn = get_db()
    cur = conn.cursor()
    if IS_POSTGRES:
        cur.execute("DELETE FROM website_items WHERE id = %s", (item_id,))
    else:
        cur.execute("DELETE FROM website_items WHERE id = ?", (item_id,))
    deleted = cur.rowcount > 0
    if deleted:
        _insert_audit(cur, "admin", "website_item_deleted", None, f"Deleted website item #{item_id}")
    conn.commit()
    cur.close()
    conn.close()
    return deleted


# ==============================================================================
# AUDIT & SYSTEM METRICS
# ==============================================================================

def _insert_audit(cur, actor, action, enquiry_id=None, details=None):
    if IS_POSTGRES:
        cur.execute(
            "INSERT INTO admin_audit_log (actor, action, enquiry_id, details) VALUES (%s, %s, %s, %s)",
            (actor, action, enquiry_id, details),
        )
    else:
        cur.execute(
            "INSERT INTO admin_audit_log (actor, action, enquiry_id, details) VALUES (?, ?, ?, ?)",
            (actor, action, enquiry_id, details),
        )


def record_audit_event(actor, action, enquiry_id=None, details=None):
    conn = get_db()
    cur = conn.cursor()
    try:
        _insert_audit(cur, actor, action, enquiry_id, details)
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()


def check_db():
    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute("SELECT 1")
        return True
    finally:
        cur.close()
        conn.close()


def get_stats():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM enquiries;")
    total = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM enquiries WHERE status = 'New';")
    new_leads = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM enquiries WHERE status = 'Contacted';")
    contacted = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM enquiries WHERE status = 'Enrolled';")
    enrolled = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM team_members;")
    team_total = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM website_items;")
    website_items_total = cur.fetchone()[0]

    # Two Options (Internship & Projects) with Tech & Non-Tech counts
    cur.execute("SELECT COUNT(*) FROM enquiries WHERE service LIKE '%Technical Internship%';")
    internship_tech = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM enquiries WHERE service LIKE '%Business & Analytics%';")
    internship_nontech = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM enquiries WHERE service LIKE '%Customized Technical Project%';")
    projects_tech = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM enquiries WHERE service LIKE '%Survey-Based%';")
    projects_nontech = cur.fetchone()[0]

    internship_total = internship_tech + internship_nontech
    projects_total = projects_tech + projects_nontech
    tech_total = internship_tech + projects_tech
    nontech_total = internship_nontech + projects_nontech
    
    cur.close()
    conn.close()
    return {
        "total": total,
        "new": new_leads,
        "contacted": contacted,
        "enrolled": enrolled,
        "team_total": team_total,
        "website_items_total": website_items_total,
        "internship_total": internship_total,
        "projects_total": projects_total,
        "internship_tech": internship_tech,
        "internship_nontech": internship_nontech,
        "projects_tech": projects_tech,
        "projects_nontech": projects_nontech,
        "tech_total": tech_total,
        "nontech_total": nontech_total,
        "db_status": DB_STATUS
    }
