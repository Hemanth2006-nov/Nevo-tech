import csv
import datetime
import hmac
import io
import json
import logging
import os
import re
import secrets
import smtplib
import urllib.error
import urllib.parse
import urllib.request
from email.message import EmailMessage

from dotenv import load_dotenv
from flask import (
    Flask, abort, jsonify, make_response, redirect, render_template, request,
    send_from_directory, session, url_for, Response
)
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.security import check_password_hash
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.utils import secure_filename

load_dotenv()

logging.basicConfig(
    level=os.environ.get("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger("nevo")

import db

APP_ENV = os.environ.get("APP_ENV", "development").lower()
IS_PRODUCTION = APP_ENV == "production"
SECRET_KEY = os.environ.get("SECRET_KEY")
ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "").strip() or "admin"
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")
ADMIN_PASSWORD_HASH = os.environ.get("ADMIN_PASSWORD_HASH")
ADMIN_AUTH_CONFIGURED = bool(ADMIN_USERNAME and (ADMIN_PASSWORD or ADMIN_PASSWORD_HASH))
TURNSTILE_SITE_KEY = os.environ.get("TURNSTILE_SITE_KEY", "").strip()
TURNSTILE_SECRET_KEY = os.environ.get("TURNSTILE_SECRET_KEY", "").strip()
TURNSTILE_REQUIRED = os.environ.get("TURNSTILE_REQUIRED", "false").lower() in {"1", "true", "yes"}

if IS_PRODUCTION:
    if not SECRET_KEY or len(SECRET_KEY) < 32:
        raise RuntimeError("Production requires a SECRET_KEY of at least 32 characters")
    if not ADMIN_PASSWORD_HASH and (not ADMIN_PASSWORD or len(ADMIN_PASSWORD) < 14):
        raise RuntimeError("Production requires ADMIN_PASSWORD_HASH or an ADMIN_PASSWORD of at least 14 characters")
if bool(TURNSTILE_SITE_KEY) != bool(TURNSTILE_SECRET_KEY):
    raise RuntimeError("Set both TURNSTILE_SITE_KEY and TURNSTILE_SECRET_KEY")
if TURNSTILE_REQUIRED and not TURNSTILE_SITE_KEY:
    raise RuntimeError("Turnstile is required but its site and secret keys are not configured")
if IS_PRODUCTION:
    email_notifications_configured = bool(
        os.environ.get("SMTP_HOST")
        and os.environ.get("SMTP_FROM")
        and os.environ.get("NOTIFICATION_EMAIL_TO")
    )
    webhook_url = os.environ.get("LEAD_WEBHOOK_URL", "").strip()
    if not email_notifications_configured and not webhook_url:
        raise RuntimeError("Production requires SMTP notification settings or LEAD_WEBHOOK_URL")
    if webhook_url and not webhook_url.startswith("https://"):
        raise RuntimeError("Production LEAD_WEBHOOK_URL must use HTTPS")

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "assets", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".svg", ".gif"}

VALID_SERVICES = {
    "Technical Internship Programs",
    "Business & Analytics Internship",
    "Customized Technical Projects & Documentation",
    "Survey-Based Projects & Research Reports",
    "General Academic Partnership",
}

app = Flask(__name__, template_folder="templates", static_folder=None)
app.secret_key = SECRET_KEY or secrets.token_urlsafe(32)
app.config.update(
    MAX_CONTENT_LENGTH=16 * 1024 * 1024,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=IS_PRODUCTION,
    SESSION_COOKIE_SAMESITE="Lax",
    PERMANENT_SESSION_LIFETIME=60 * 60 * 8,
)

if os.environ.get("TRUST_PROXY", "false").lower() in {"1", "true", "yes"}:
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)

limiter = Limiter(
    get_remote_address,
    app=app,
    storage_uri=os.environ.get("RATELIMIT_STORAGE_URI", "memory://"),
    default_limits=[],
)

try:
    db.init_db()
except Exception:
    logger.exception("Database schema initialization failed")
    raise


def _admin_password_matches(candidate):
    if ADMIN_PASSWORD_HASH:
        try:
            return check_password_hash(ADMIN_PASSWORD_HASH, candidate)
        except ValueError:
            logger.error("ADMIN_PASSWORD_HASH is not a valid Werkzeug password hash")
            return False
    return bool(ADMIN_PASSWORD) and hmac.compare_digest(candidate, ADMIN_PASSWORD)


def _csrf_token():
    token = session.get("_csrf_token")
    if not token:
        token = secrets.token_urlsafe(32)
        session["_csrf_token"] = token
    return token


def _valid_csrf_token():
    expected = session.get("_csrf_token", "")
    supplied = request.headers.get("X-CSRFToken") or request.form.get("csrf_token", "")
    return bool(expected and supplied and hmac.compare_digest(expected, supplied))


def _require_admin():
    if not session.get("is_admin"):
        return jsonify({"success": False, "error": "Unauthorized"}), 401
    if not _valid_csrf_token():
        return jsonify({"success": False, "error": "Invalid or missing CSRF token"}), 403
    return None


def _verify_turnstile(token):
    if not TURNSTILE_SITE_KEY:
        return not TURNSTILE_REQUIRED
    if not token:
        return False

    body = urllib.parse.urlencode({
        "secret": TURNSTILE_SECRET_KEY,
        "response": token,
        "remoteip": request.remote_addr or "",
    }).encode("utf-8")
    req = urllib.request.Request(
        "https://challenges.cloudflare.com/turnstile/v0/siteverify",
        data=body,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            result = json.loads(response.read(4096).decode("utf-8"))
        return isinstance(result, dict) and result.get("success") is True
    except (urllib.error.URLError, TimeoutError, ValueError, UnicodeDecodeError):
        logger.exception("Turnstile verification request failed")
        return False


def _send_notifications(enquiry, enquiry_id):
    recipient = os.environ.get("NOTIFICATION_EMAIL_TO", "").strip()
    smtp_host = os.environ.get("SMTP_HOST", "").strip()
    if recipient and smtp_host:
        message = EmailMessage()
        message["Subject"] = f"New NEVO TECH enquiry #{enquiry_id}"
        message["From"] = os.environ.get("SMTP_FROM", os.environ.get("SMTP_USER", "")).strip()
        message["To"] = recipient
        message.set_content(
            "A new enquiry was saved.\n\n"
            f"Name: {enquiry['fullName']}\n"
            f"Email: {enquiry['email']}\n"
            f"Phone: {enquiry['phone']}\n"
            f"Service: {enquiry['service']}\n"
            f"Institution: {enquiry['institution']}\n"
            f"Domain: {enquiry['domain']}\n"
            f"Message: {enquiry['message']}\n"
            f"Enquiry ID: {enquiry_id}\n"
        )
        try:
            port = int(os.environ.get("SMTP_PORT", "587"))
            use_ssl = os.environ.get("SMTP_USE_SSL", "false").lower() in {"1", "true", "yes"}
            smtp_class = smtplib.SMTP_SSL if use_ssl else smtplib.SMTP
            with smtp_class(smtp_host, port, timeout=5) as smtp:
                if not use_ssl and os.environ.get("SMTP_USE_TLS", "true").lower() in {"1", "true", "yes"}:
                    smtp.starttls()
                smtp_user = os.environ.get("SMTP_USER", "")
                smtp_password = os.environ.get("SMTP_PASSWORD", "")
                if smtp_user:
                    smtp.login(smtp_user, smtp_password)
                smtp.send_message(message)
        except (OSError, smtplib.SMTPException, ValueError):
            logger.exception("Email notification failed for enquiry id=%s", enquiry_id)

    webhook_url = os.environ.get("LEAD_WEBHOOK_URL", "").strip()
    if webhook_url:
        payload = json.dumps({
            "event": "enquiry.created",
            "id": enquiry_id,
            "enquiry": enquiry,
        }).encode("utf-8")
        req = urllib.request.Request(
            webhook_url,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=5) as response:
                if response.status >= 400:
                    logger.error("Lead webhook returned HTTP %s for enquiry id=%s", response.status, enquiry_id)
        except (urllib.error.URLError, TimeoutError, ValueError):
            logger.exception("Lead webhook failed for enquiry id=%s", enquiry_id)


@app.before_request
def ensure_csrf_token():
    if request.endpoint in {"admin_login", "admin_dashboard"}:
        _csrf_token()


@app.after_request
def add_security_headers(response):
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("X-Frame-Options", "DENY")
    response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
    response.headers.setdefault("Permissions-Policy", "camera=(), microphone=(), geolocation=()")
    if request.path.startswith("/admin") or request.endpoint in {"admin_dashboard", "admin_login"}:
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
    if request.is_secure:
        response.headers.setdefault("Strict-Transport-Security", "max-age=31536000; includeSubDomains")
    return response


@app.get("/")
def index():
    return send_from_directory(".", "index.html")


@app.get("/api/public-config")
def public_config():
    return jsonify({
        "turnstileSiteKey": TURNSTILE_SITE_KEY,
        "turnstileRequired": TURNSTILE_REQUIRED,
    })


@app.get("/health/live")
def health_live():
    return jsonify({"status": "ok"})


@app.get("/health/ready")
def health_ready():
    try:
        db.check_db()
    except Exception:
        logger.exception("Readiness database check failed")
        return jsonify({"status": "not_ready", "database": "unavailable"}), 503
    return jsonify({"status": "ready", "database": db.DB_STATUS})


@app.route("/<path:path>")
def static_proxy(path):
    if path.startswith("assets/") and not any(part.startswith(".") for part in path.split("/")):
        return send_from_directory(".", path)
    if "/" not in path and os.path.splitext(path)[1].lower() in {".html", ".css", ".js"}:
        if os.path.isfile(path):
            return send_from_directory(".", path)
    abort(404)


@app.errorhandler(404)
def not_found(_error):
    if request.path.startswith("/api/") or request.path.startswith("/health/"):
        return jsonify({"success": False, "error": "Not found"}), 404
    return "<!doctype html><title>Not found</title><h1>Page not found</h1>", 404


@app.errorhandler(413)
def request_too_large(_error):
    return jsonify({"success": False, "error": "Request is too large"}), 413


@app.errorhandler(429)
def rate_limit_exceeded(_error):
    if request.path.startswith("/api/"):
        return jsonify({"success": False, "error": "Too many requests. Please try again later."}), 429
    return "<!doctype html><title>Too many requests</title><h1>Please try again later</h1>", 429


@app.errorhandler(500)
def internal_server_error(_error):
    logger.error("Request failed with HTTP 500")
    if request.path.startswith("/api/"):
        return jsonify({"success": False, "error": "An internal error occurred. Please try again later."}), 500
    return "<!doctype html><title>Server error</title><h1>Something went wrong</h1>", 500


# ==============================================================================
# IMAGE UPLOAD API (Photos for Website & People)
# ==============================================================================

@app.post("/api/upload-image")
def upload_image():
    auth_error = _require_admin()
    if auth_error:
        return auth_error

    file = request.files.get("photo") or request.files.get("image") or request.files.get("file")
    if not file or not file.filename:
        return jsonify({"success": False, "error": "No image file provided"}), 400

    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_IMAGE_EXTENSIONS:
        return jsonify({
            "success": False,
            "error": f"Invalid image format. Allowed formats: {', '.join(sorted(ALLOWED_IMAGE_EXTENSIONS))}"
        }), 400

    raw_base = os.path.splitext(file.filename)[0]
    safe_base = secure_filename(raw_base)[:30] or "photo"
    filename = f"{safe_base}_{secrets.token_hex(4)}{ext}"
    dest_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(dest_path)

    return jsonify({
        "success": True,
        "message": "Image uploaded successfully",
        "url": f"/assets/uploads/{filename}"
    })


# ==============================================================================
# ENQUIRIES API (Public submission + Admin listing, modifying, and creating)
# ==============================================================================

@app.post("/api/enquiries")
@limiter.limit("5 per minute")
def submit_enquiry():
    data = request.get_json(silent=True) if request.is_json else request.form.to_dict()
    if not isinstance(data, dict) or not data:
        return jsonify({"success": False, "error": "A valid enquiry is required"}), 400

    if str(data.get("website", "")).strip():
        return jsonify({"success": True, "message": "Enquiry submitted successfully"}), 202
    if not _verify_turnstile(str(data.get("captchaToken", "")).strip()):
        return jsonify({"success": False, "error": "Please complete the verification and try again."}), 400

    fields = {
        "fullName": str(data.get("fullName", "")).strip(),
        "email": str(data.get("email", "")).strip(),
        "phone": str(data.get("phone", "")).strip(),
        "service": str(data.get("service", "")).strip(),
        "institution": str(data.get("institution", "")).strip(),
        "domain": str(data.get("domain", "")).strip(),
        "message": str(data.get("message", "")).strip(),
    }
    if not fields["fullName"] or len(fields["fullName"]) > 120:
        return jsonify({"success": False, "error": "Enter a name no longer than 120 characters."}), 400
    if len(fields["email"]) > 254 or not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", fields["email"]):
        return jsonify({"success": False, "error": "Enter a valid email address."}), 400
    phone_digits = re.sub(r"\D", "", fields["phone"])
    if (
        not re.fullmatch(r"[0-9+().\-\s]{7,30}", fields["phone"])
        or not 7 <= len(phone_digits) <= 15
    ):
        return jsonify({"success": False, "error": "Enter a valid phone number."}), 400
    if fields["service"] not in VALID_SERVICES:
        return jsonify({"success": False, "error": "Select a service."}), 400
    if any(len(fields[field]) > limit for field, limit in (
        ("institution", 160), ("domain", 160), ("message", 4000)
    )):
        return jsonify({"success": False, "error": "One or more fields exceed the allowed length."}), 400

    try:
        saved = db.insert_enquiry(fields)
    except Exception:
        logger.exception("Could not save an enquiry")
        return jsonify({"success": False, "error": "We could not save your enquiry. Please try again shortly."}), 503

    _send_notifications(fields, saved["id"])
    return jsonify({
        "success": True,
        "message": "Enquiry submitted successfully. Our team will contact you shortly.",
        "data": saved,
    }), 201


@app.get("/api/enquiries")
def list_enquiries():
    if not session.get("is_admin"):
        return jsonify({"success": False, "error": "Unauthorized"}), 401
    enquiries = db.get_all_enquiries(
        service_filter=request.args.get("service"),
        status_filter=request.args.get("status"),
        search=request.args.get("search"),
        category=request.args.get("category"),
        track=request.args.get("track"),
    )
    return jsonify({"success": True, "enquiries": enquiries})


@app.get("/api/enquiries/<int:enquiry_id>")
def get_single_enquiry(enquiry_id):
    if not session.get("is_admin"):
        return jsonify({"success": False, "error": "Unauthorized"}), 401
    enquiry = db.get_enquiry_by_id(enquiry_id)
    if not enquiry:
        return jsonify({"success": False, "error": "Enquiry not found"}), 404
    return jsonify({"success": True, "enquiry": enquiry})


@app.patch("/api/enquiries/<int:enquiry_id>")
def update_enquiry_status_route(enquiry_id):
    auth_error = _require_admin()
    if auth_error:
        return auth_error

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"success": False, "error": "A valid JSON object is required."}), 400
    status = data.get("status")
    notes = data.get("notes")
    allowed_statuses = {"New", "Contacted", "In Review", "In Progress", "Enrolled", "Closed"}
    if not isinstance(status, str) or status not in allowed_statuses:
        return jsonify({"success": False, "error": "Choose a valid enquiry status."}), 400
    if notes is not None and (not isinstance(notes, str) or len(notes) > 4000):
        return jsonify({"success": False, "error": "Notes must be no longer than 4000 characters."}), 400

    changed = db.update_enquiry_status(enquiry_id, status, notes)
    if not changed:
        return jsonify({"success": False, "error": "Enquiry not found."}), 404
    return jsonify({"success": True, "message": "Status updated successfully"})


@app.put("/api/enquiries/<int:enquiry_id>")
def modify_enquiry(enquiry_id):
    auth_error = _require_admin()
    if auth_error:
        return auth_error

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"success": False, "error": "A valid JSON object is required."}), 400

    full_name = str(data.get("fullName", "")).strip()
    email = str(data.get("email", "")).strip()
    phone = str(data.get("phone", "")).strip()
    service = str(data.get("service", "")).strip()
    institution = str(data.get("institution", "")).strip()
    domain = str(data.get("domain", "")).strip()
    message = str(data.get("message", "")).strip()
    status = str(data.get("status", "New")).strip()
    notes = str(data.get("notes", "")).strip()

    if not full_name or len(full_name) > 120:
        return jsonify({"success": False, "error": "Enter a name no longer than 120 characters."}), 400
    if len(email) > 254 or not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        return jsonify({"success": False, "error": "Enter a valid email address."}), 400
    phone_digits = re.sub(r"\D", "", phone)
    if not re.fullmatch(r"[0-9+().\-\s]{7,30}", phone) or not 7 <= len(phone_digits) <= 15:
        return jsonify({"success": False, "error": "Enter a valid phone number."}), 400
    if service not in VALID_SERVICES:
        return jsonify({"success": False, "error": "Select a valid service track."}), 400

    allowed_statuses = {"New", "Contacted", "In Review", "In Progress", "Enrolled", "Closed"}
    if status not in allowed_statuses:
        return jsonify({"success": False, "error": "Choose a valid enquiry status."}), 400
    if len(notes) > 4000:
        return jsonify({"success": False, "error": "Notes must be no longer than 4000 characters."}), 400

    changed = db.update_enquiry(enquiry_id, {
        "fullName": full_name,
        "email": email,
        "phone": phone,
        "service": service,
        "institution": institution,
        "domain": domain,
        "message": message,
        "status": status,
        "notes": notes,
    })
    if not changed:
        return jsonify({"success": False, "error": "Enquiry not found."}), 404
    return jsonify({"success": True, "message": "Enquiry details updated successfully"})


@app.post("/api/admin/enquiries")
def admin_create_enquiry():
    auth_error = _require_admin()
    if auth_error:
        return auth_error

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"success": False, "error": "A valid JSON object is required."}), 400

    full_name = str(data.get("fullName", "")).strip()
    email = str(data.get("email", "")).strip()
    phone = str(data.get("phone", "")).strip()
    service = str(data.get("service", "")).strip()
    institution = str(data.get("institution", "")).strip()
    domain = str(data.get("domain", "")).strip()
    message = str(data.get("message", "")).strip()
    status = str(data.get("status", "New")).strip()
    notes = str(data.get("notes", "")).strip()

    if not full_name or len(full_name) > 120:
        return jsonify({"success": False, "error": "Enter a name no longer than 120 characters."}), 400
    if len(email) > 254 or not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        return jsonify({"success": False, "error": "Enter a valid email address."}), 400
    phone_digits = re.sub(r"\D", "", phone)
    if not re.fullmatch(r"[0-9+().\-\s]{7,30}", phone) or not 7 <= len(phone_digits) <= 15:
        return jsonify({"success": False, "error": "Enter a valid phone number."}), 400
    if service not in VALID_SERVICES:
        return jsonify({"success": False, "error": "Select a valid service track."}), 400

    allowed_statuses = {"New", "Contacted", "In Review", "In Progress", "Enrolled", "Closed"}
    if status not in allowed_statuses:
        status = "New"

    saved = db.create_enquiry_by_admin({
        "fullName": full_name,
        "email": email,
        "phone": phone,
        "service": service,
        "institution": institution,
        "domain": domain,
        "message": message,
        "status": status,
        "notes": notes,
    })
    return jsonify({"success": True, "message": "Enquiry added successfully", "data": saved}), 201


@app.delete("/api/enquiries/<int:enquiry_id>")
def delete_enquiry_route(enquiry_id):
    auth_error = _require_admin()
    if auth_error:
        return auth_error
    if not db.delete_enquiry(enquiry_id):
        return jsonify({"success": False, "error": "Enquiry not found."}), 404
    return jsonify({"success": True, "message": "Enquiry deleted successfully"})


@app.delete("/api/admin/enquiries/clear-all")
def clear_all_enquiries_route():
    auth_error = _require_admin()
    if auth_error:
        return auth_error
    db.clear_all_enquiries()
    return jsonify({"success": True, "message": "All inquiries have been cleared successfully."})


# ==============================================================================
# TEAM MEMBERS API ("Adding new peoples")
# ==============================================================================

@app.get("/api/team")
def get_public_team():
    team = db.get_all_team_members(active_only=True)
    return jsonify({"success": True, "team": team})


@app.get("/api/admin/team")
def get_admin_team():
    if not session.get("is_admin"):
        return jsonify({"success": False, "error": "Unauthorized"}), 401
    team = db.get_all_team_members(active_only=False)
    return jsonify({"success": True, "team": team})


@app.post("/api/admin/team")
def create_team_member():
    auth_error = _require_admin()
    if auth_error:
        return auth_error

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"success": False, "error": "A valid JSON object is required."}), 400

    name = str(data.get("name", "")).strip()
    role = str(data.get("role", "")).strip()
    if not name or len(name) > 120:
        return jsonify({"success": False, "error": "Enter a name up to 120 characters."}), 400
    if not role or len(role) > 120:
        return jsonify({"success": False, "error": "Enter a role/title up to 120 characters."}), 400

    saved = db.insert_team_member(data)
    return jsonify({"success": True, "message": "Person added successfully", "data": saved}), 201


@app.put("/api/admin/team/<int:member_id>")
def update_team_member_route(member_id):
    auth_error = _require_admin()
    if auth_error:
        return auth_error

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"success": False, "error": "A valid JSON object is required."}), 400

    name = str(data.get("name", "")).strip()
    role = str(data.get("role", "")).strip()
    if not name or len(name) > 120:
        return jsonify({"success": False, "error": "Enter a name up to 120 characters."}), 400
    if not role or len(role) > 120:
        return jsonify({"success": False, "error": "Enter a role/title up to 120 characters."}), 400

    changed = db.update_team_member(member_id, data)
    if not changed:
        return jsonify({"success": False, "error": "Person not found."}), 404
    return jsonify({"success": True, "message": "Person details updated successfully"})


@app.delete("/api/admin/team/<int:member_id>")
def delete_team_member_route(member_id):
    auth_error = _require_admin()
    if auth_error:
        return auth_error
    if not db.delete_team_member(member_id):
        return jsonify({"success": False, "error": "Person not found."}), 404
    return jsonify({"success": True, "message": "Person deleted successfully"})


# ==============================================================================
# WEBSITE DETAILS & PHOTOS (Showcase / Website Items)
# ==============================================================================

@app.get("/api/website-items")
def get_public_website_items():
    items = db.get_all_website_items(active_only=True)
    return jsonify({"success": True, "items": items})


@app.get("/api/admin/website-items")
def get_admin_website_items():
    if not session.get("is_admin"):
        return jsonify({"success": False, "error": "Unauthorized"}), 401
    items = db.get_all_website_items(active_only=False)
    return jsonify({"success": True, "items": items})


@app.post("/api/admin/website-items")
def create_website_item():
    auth_error = _require_admin()
    if auth_error:
        return auth_error

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"success": False, "error": "A valid JSON object is required."}), 400

    title = str(data.get("title", "")).strip()
    description = str(data.get("description", "")).strip()
    photo_url = str(data.get("photo_url", "")).strip()
    if not title or len(title) > 160:
        return jsonify({"success": False, "error": "Enter a title up to 160 characters."}), 400
    if not description:
        return jsonify({"success": False, "error": "Enter a description or details for this item."}), 400
    if not photo_url:
        return jsonify({"success": False, "error": "Provide a photo or upload an image."}), 400

    saved = db.insert_website_item(data)
    return jsonify({"success": True, "message": "Website item added successfully", "data": saved}), 201


@app.put("/api/admin/website-items/<int:item_id>")
def update_website_item_route(item_id):
    auth_error = _require_admin()
    if auth_error:
        return auth_error

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"success": False, "error": "A valid JSON object is required."}), 400

    title = str(data.get("title", "")).strip()
    description = str(data.get("description", "")).strip()
    photo_url = str(data.get("photo_url", "")).strip()
    if not title or len(title) > 160:
        return jsonify({"success": False, "error": "Enter a title up to 160 characters."}), 400
    if not description:
        return jsonify({"success": False, "error": "Enter a description or details for this item."}), 400
    if not photo_url:
        return jsonify({"success": False, "error": "Provide a photo or upload an image."}), 400

    changed = db.update_website_item(item_id, data)
    if not changed:
        return jsonify({"success": False, "error": "Website item not found."}), 404
    return jsonify({"success": True, "message": "Website item updated successfully"})


@app.delete("/api/admin/website-items/<int:item_id>")
def delete_website_item_route(item_id):
    auth_error = _require_admin()
    if auth_error:
        return auth_error
    if not db.delete_website_item(item_id):
        return jsonify({"success": False, "error": "Website item not found."}), 404
    return jsonify({"success": True, "message": "Website item deleted successfully"})


# ==============================================================================
# ADMIN AUTH & DASHBOARD
# ==============================================================================

@app.route("/admin/login", methods=["GET", "POST"])
@limiter.limit("5 per minute", methods=["POST"])
def admin_login():
    error = None
    if not ADMIN_AUTH_CONFIGURED:
        return render_template(
            "admin_login.html",
            error="Admin login is not configured. Set ADMIN_USERNAME and an admin password locally before signing in.",
            csrf_token=_csrf_token(),
            login_enabled=False,
        ), 503
    if request.method == "POST":
        if not _valid_csrf_token():
            return render_template(
                "admin_login.html",
                error="Your session expired. Please try again.",
                csrf_token=_csrf_token(),
                login_enabled=True,
            ), 400
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        if (
            hmac.compare_digest(username.encode("utf-8"), ADMIN_USERNAME.encode("utf-8"))
            and _admin_password_matches(password)
        ):
            session.clear()
            session["is_admin"] = True
            session.permanent = True
            _csrf_token()
            db.record_audit_event(ADMIN_USERNAME, "login_success")
            return redirect(url_for("admin_dashboard"))
        error = "Invalid administrator username or password. Please try again."

    return render_template(
        "admin_login.html",
        error=error,
        csrf_token=_csrf_token(),
        login_enabled=True,
    )


@app.post("/admin/logout")
def admin_logout():
    if not _valid_csrf_token():
        abort(403)
    if session.get("is_admin"):
        db.record_audit_event("admin", "logout")
    session.clear()
    return redirect(url_for("admin_login"))


@app.get("/admin")
@app.get("/admin/dashboard")
def admin_dashboard():
    if not session.get("is_admin"):
        return redirect(url_for("admin_login"))
    service_filter = request.args.get("service")
    category_filter = request.args.get("category")
    track_filter = request.args.get("track")
    status_filter = request.args.get("status")
    search = request.args.get("search")
    response = make_response(render_template(
        "admin.html",
        enquiries=db.get_all_enquiries(),
        team_members=db.get_all_team_members(),
        website_items=db.get_all_website_items(),
        stats=db.get_stats(),
        service_filter=service_filter,
        category_filter=category_filter,
        track_filter=track_filter,
        status_filter=status_filter,
        search=search,
        csrf_token=_csrf_token(),
    ))
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


@app.post("/admin/export-csv")
def export_csv():
    if not session.get("is_admin"):
        return redirect(url_for("admin_login"))
    if not _valid_csrf_token():
        abort(403)
    db.record_audit_event("admin", "csv_export")
    enquiries = db.get_all_enquiries()
    output = io.StringIO()
    writer = csv.writer(output)

    def safe_cell(value):
        text = "" if value is None else str(value)
        if text.startswith(("=", "+", "-", "@", "\t", "\r")):
            return "'" + text
        return text

    writer.writerow([
        "ID", "Date", "Full Name", "Email", "Phone",
        "Service Track", "Institution", "Domain", "Message", "Status",
    ])
    for item in enquiries:
        writer.writerow([
            safe_cell(item.get("id")), safe_cell(item.get("created_at")),
            safe_cell(item.get("full_name")), safe_cell(item.get("email")),
            safe_cell(item.get("phone")), safe_cell(item.get("service")),
            safe_cell(item.get("institution", "")), safe_cell(item.get("domain", "")),
            safe_cell(item.get("message", "").replace("\n", " ")),
            safe_cell(item.get("status", "New")),
        ])
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=nevo_tech_enquiries.csv"},
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    logger.info("Starting NEVO TECH Flask Server on port %s", port)
    app.run(host="0.0.0.0", port=port, debug=False)
