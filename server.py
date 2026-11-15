import os
import csv
import io
from flask import (
    Flask, render_template, request, jsonify, redirect, 
    url_for, session, send_from_directory, Response
)
from dotenv import load_dotenv
import db

load_dotenv()

app = Flask(__name__, template_folder="templates", static_folder=".")
app.secret_key = os.environ.get("SECRET_KEY", "nevo_secret_key_prod_2026")

ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin123")

# Initialize database schema on startup
with app.app_context():
    try:
        db.init_db()
    except Exception as e:
        print("[Startup Warning] DB init error:", e)


# =====================================================================
# STATIC & WEBSITE ROUTES
# =====================================================================
@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/<path:path>")
def static_proxy(path):
    if os.path.exists(path):
        return send_from_directory(".", path)
    return send_from_directory(".", "index.html")


# =====================================================================
# API ROUTES (ENQUIRIES SUBMISSION & MANAGEMENT)
# =====================================================================
@app.route("/api/enquiries", methods=["POST"])
def submit_enquiry():
    try:
        data = request.get_json(force=True) if request.is_json else request.form.to_dict()
        if not data:
            return jsonify({"success": False, "error": "No data received"}), 400

        full_name = data.get("fullName", "").strip()
        email = data.get("email", "").strip()
        phone = data.get("phone", "").strip()

        if not full_name or not email or not phone:
            return jsonify({"success": False, "error": "Name, email, and phone are required."}), 400

        res = db.insert_enquiry(data)
        return jsonify({
            "success": True,
            "message": "Enquiry submitted successfully! Our academic coordinator will contact you shortly.",
            "data": res
        }), 201

    except Exception as e:
        print("[API Error] submit_enquiry error:", e)
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/enquiries", methods=["GET"])
def list_enquiries():
    if not session.get("is_admin"):
        return jsonify({"success": False, "error": "Unauthorized"}), 401
    
    service = request.args.get("service")
    status = request.args.get("status")
    search = request.args.get("search")
    enquiries = db.get_all_enquiries(service, status, search)
    return jsonify({"success": True, "enquiries": enquiries})


@app.route("/api/enquiries/<int:enquiry_id>", methods=["PATCH"])
def update_enquiry(enquiry_id):
    if not session.get("is_admin"):
        return jsonify({"success": False, "error": "Unauthorized"}), 401

    data = request.get_json() or {}
    status = data.get("status")
    notes = data.get("notes")

    if not status:
        return jsonify({"success": False, "error": "Status is required"}), 400

    db.update_enquiry_status(enquiry_id, status, notes)
    return jsonify({"success": True, "message": "Status updated successfully"})


@app.route("/api/enquiries/<int:enquiry_id>", methods=["DELETE"])
def delete_enquiry_route(enquiry_id):
    if not session.get("is_admin"):
        return jsonify({"success": False, "error": "Unauthorized"}), 401

    db.delete_enquiry(enquiry_id)
    return jsonify({"success": True, "message": "Enquiry deleted successfully"})


# =====================================================================
# ADMIN DASHBOARD & AUTHENTICATION
# =====================================================================
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    error = None
    if request.method == "POST":
        pwd = request.form.get("password", "")
        if pwd == ADMIN_PASSWORD:
            session["is_admin"] = True
            return redirect(url_for("admin_dashboard"))
        else:
            error = "Invalid administrator password. Please try again."

    return render_template("admin_login.html", error=error)


@app.route("/admin/logout")
def admin_logout():
    session.pop("is_admin", None)
    return redirect(url_for("admin_login"))


@app.route("/admin")
@app.route("/admin/dashboard")
def admin_dashboard():
    if not session.get("is_admin"):
        return redirect(url_for("admin_login"))

    service_filter = request.args.get("service")
    status_filter = request.args.get("status")
    search = request.args.get("search")

    enquiries = db.get_all_enquiries(service_filter, status_filter, search)
    stats = db.get_stats()

    return render_template(
        "admin.html",
        enquiries=enquiries,
        stats=stats,
        service_filter=service_filter,
        status_filter=status_filter,
        search=search
    )


@app.route("/admin/export-csv")
def export_csv():
    if not session.get("is_admin"):
        return redirect(url_for("admin_login"))

    enquiries = db.get_all_enquiries()
    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow([
        "ID", "Date", "Full Name", "Email", "Phone", 
        "Service Track", "Institution", "Domain", "Message", "Status"
    ])

    for item in enquiries:
        writer.writerow([
            item.get("id"),
            item.get("created_at"),
            item.get("full_name"),
            item.get("email"),
            item.get("phone"),
            item.get("service"),
            item.get("institution", ""),
            item.get("domain", ""),
            item.get("message", "").replace("\n", " "),
            item.get("status", "New")
        ])

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=nevo_tech_enquiries.csv"}
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting NEVO TECH Flask Server on port {port}...")
    app.run(host="0.0.0.0", port=port, debug=False)
