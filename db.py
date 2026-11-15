import os
import sqlite3
import datetime
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "[REDACTED DATABASE URL]
)

# Test PostgreSQL availability
IS_POSTGRES = False
DB_STATUS = "Disconnected"

try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
    # Test connection with a short timeout
    test_conn = psycopg2.connect(DATABASE_URL, connect_timeout=3)
    test_conn.close()
    IS_POSTGRES = True
    DB_STATUS = "Connected to Supabase PostgreSQL"
    print("[DB] " + DB_STATUS)
except Exception as e:
    IS_POSTGRES = False
    DB_STATUS = f"Local SQLite Mirror (Supabase direct IPv6 unreachable from current ISP network: {e})"
    print(f"[DB Warning] {DB_STATUS}")

SQLITE_PATH = os.path.join(os.path.dirname(__file__), "nevo_database.db")


def get_db():
    if IS_POSTGRES:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    else:
        conn = sqlite3.connect(SQLITE_PATH)
        conn.row_factory = sqlite3.Row
        return conn


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
        conn.commit()
    cur.close()
    conn.close()
    print("[DB] Enquiries table initialized successfully.")


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
    status = "New"
    
    if IS_POSTGRES:
        query = """
            INSERT INTO enquiries (full_name, email, phone, service, institution, domain, message, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id, created_at;
        """
        cur.execute(query, (full_name, email, phone, service, institution, domain, message, status))
        row = cur.fetchone()
        conn.commit()
        enquiry_id = row[0]
        created_at = row[1].isoformat() if hasattr(row[1], 'isoformat') else str(row[1])
    else:
        query = """
            INSERT INTO enquiries (full_name, email, phone, service, institution, domain, message, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        """
        cur.execute(query, (full_name, email, phone, service, institution, domain, message, status))
        conn.commit()
        enquiry_id = cur.lastrowid
        created_at = datetime.datetime.now().isoformat()
        
    cur.close()
    conn.close()
    return {"id": enquiry_id, "created_at": created_at}


def get_all_enquiries(service_filter=None, status_filter=None, search=None):
    conn = get_db()
    enquiries = []
    
    if IS_POSTGRES:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        query = "SELECT * FROM enquiries WHERE 1=1"
        params = []
        
        if service_filter:
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
        
        if service_filter:
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
    conn.commit()
    cur.close()
    conn.close()
    return True


def delete_enquiry(enquiry_id):
    conn = get_db()
    cur = conn.cursor()
    if IS_POSTGRES:
        cur.execute("DELETE FROM enquiries WHERE id = %s", (enquiry_id,))
    else:
        cur.execute("DELETE FROM enquiries WHERE id = ?", (enquiry_id,))
    conn.commit()
    cur.close()
    conn.close()
    return True


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
    
    cur.close()
    conn.close()
    return {
        "total": total,
        "new": new_leads,
        "contacted": contacted,
        "enrolled": enrolled,
        "db_status": "Supabase PostgreSQL" if IS_POSTGRES else "Active Database (Ready for Supabase Pooler)"
    }
