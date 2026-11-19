import io
import pytest
import server


@pytest.fixture
def logged_in_admin(monkeypatch):
    server.app.config.update(TESTING=True)
    monkeypatch.setattr(server, "ADMIN_AUTH_CONFIGURED", True)
    monkeypatch.setattr(server, "ADMIN_USERNAME", "admin")
    monkeypatch.setattr(server, "_admin_password_matches", lambda p: True)
    client = server.app.test_client()
    with client.session_transaction() as sess:
        sess["is_admin"] = True
        sess["_csrf_token"] = "valid-csrf-token"
    return client


def test_admin_modify_enquiry_flow(logged_in_admin):
    # 1. Add a test enquiry
    create_res = logged_in_admin.post(
        "/api/admin/enquiries",
        json={
            "fullName": "Priya Sen",
            "email": "priya@example.com",
            "phone": "+91 98888 77777",
            "service": "Business & Analytics Internship",
            "institution": "BMS College of Engineering",
            "domain": "Financial Analytics",
            "status": "New",
            "notes": "Initial phone enquiry",
            "message": "Interested in PowerBI and SQL tracks"
        },
        headers={"X-CSRFToken": "valid-csrf-token"}
    )
    assert create_res.status_code == 201
    enquiry_id = create_res.get_json()["data"]["id"]

    # 2. Fetch single enquiry
    get_res = logged_in_admin.get(f"/api/enquiries/{enquiry_id}")
    assert get_res.status_code == 200
    assert get_res.get_json()["enquiry"]["full_name"] == "Priya Sen"

    # 3. Modify full enquiry details
    put_res = logged_in_admin.put(
        f"/api/enquiries/{enquiry_id}",
        json={
            "fullName": "Priya Sen-Gupta",
            "email": "priya.sengupta@example.com",
            "phone": "+91 98888 77777",
            "service": "Business & Analytics Internship",
            "institution": "BMS Institute of Technology",
            "domain": "Executive Data Dashboards",
            "status": "In Progress",
            "notes": "Completed counseling session. Confirmed batch dates.",
            "message": "Updated requirements for Python and PowerBI"
        },
        headers={"X-CSRFToken": "valid-csrf-token"}
    )
    assert put_res.status_code == 200
    assert put_res.get_json()["success"] is True

    # 4. Verify modification persisted
    get_res2 = logged_in_admin.get(f"/api/enquiries/{enquiry_id}")
    assert get_res2.status_code == 200
    assert get_res2.get_json()["enquiry"]["full_name"] == "Priya Sen-Gupta"
    assert get_res2.get_json()["enquiry"]["status"] == "In Progress"

    # 5. Delete enquiry
    del_res = logged_in_admin.delete(
        f"/api/enquiries/{enquiry_id}",
        headers={"X-CSRFToken": "valid-csrf-token"}
    )
    assert del_res.status_code == 200


def test_team_member_crud_flow(logged_in_admin):
    # 1. Create team member
    create_res = logged_in_admin.post(
        "/api/admin/team",
        json={
            "name": "Prof. David Miller",
            "role": "Visiting Research Fellow",
            "department": "Survey & Research",
            "photo_url": "/assets/mentor-sneha.svg",
            "bio": "Specialist in structural equation modeling and econometrics.",
            "email": "david.m@example.com",
            "linkedin_url": "https://linkedin.com",
            "display_order": 10,
            "is_active": 1
        },
        headers={"X-CSRFToken": "valid-csrf-token"}
    )
    assert create_res.status_code == 201
    member_id = create_res.get_json()["data"]["id"]

    # 2. Verify in public team endpoint
    pub_res = logged_in_admin.get("/api/team")
    assert pub_res.status_code == 200
    names = [m["name"] for m in pub_res.get_json()["team"]]
    assert "Prof. David Miller" in names

    # 3. Update team member
    put_res = logged_in_admin.put(
        f"/api/admin/team/{member_id}",
        json={
            "name": "Prof. David Miller, Ph.D.",
            "role": "Distinguished Senior Fellow",
            "department": "Survey & Research",
            "photo_url": "/assets/mentor-sneha.svg",
            "bio": "Updated biography with 20+ journal publications.",
            "email": "david.miller@example.com",
            "linkedin_url": "https://linkedin.com",
            "display_order": 10,
            "is_active": 1
        },
        headers={"X-CSRFToken": "valid-csrf-token"}
    )
    assert put_res.status_code == 200

    # 4. Delete team member
    del_res = logged_in_admin.delete(
        f"/api/admin/team/{member_id}",
        headers={"X-CSRFToken": "valid-csrf-token"}
    )
    assert del_res.status_code == 200


def test_website_items_crud_flow(logged_in_admin):
    # 1. Create showcase item
    create_res = logged_in_admin.post(
        "/api/admin/website-items",
        json={
            "title": "Autonomous Drone Telemetry Rig",
            "category": "Lab & Campus",
            "description": "Custom PX4 autopilot flight computers and real-time lidar telemetry.",
            "photo_url": "/assets/office-render.svg",
            "badge_text": "AEROSPACE LAB",
            "link_url": "#projects",
            "display_order": 8,
            "is_active": 1
        },
        headers={"X-CSRFToken": "valid-csrf-token"}
    )
    assert create_res.status_code == 201
    item_id = create_res.get_json()["data"]["id"]

    # 2. Verify in public endpoint
    pub_res = logged_in_admin.get("/api/website-items")
    assert pub_res.status_code == 200
    titles = [x["title"] for x in pub_res.get_json()["items"]]
    assert "Autonomous Drone Telemetry Rig" in titles

    # 3. Update showcase item
    put_res = logged_in_admin.put(
        f"/api/admin/website-items/{item_id}",
        json={
            "title": "Autonomous Drone Telemetry Rig (V2)",
            "category": "Lab & Campus",
            "description": "Updated description with centimeter-level RTK GPS telemetry.",
            "photo_url": "/assets/office-render.svg",
            "badge_text": "ROBOTICS LAB",
            "link_url": "#projects",
            "display_order": 8,
            "is_active": 1
        },
        headers={"X-CSRFToken": "valid-csrf-token"}
    )
    assert put_res.status_code == 200

    # 4. Delete showcase item
    del_res = logged_in_admin.delete(
        f"/api/admin/website-items/{item_id}",
        headers={"X-CSRFToken": "valid-csrf-token"}
    )
    assert del_res.status_code == 200


def test_image_upload_endpoint(logged_in_admin):
    # Upload simulated PNG image
    data = {
        "photo": (io.BytesIO(b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15c4"), "test_avatar.png")
    }
    res = logged_in_admin.post(
        "/api/upload-image",
        data=data,
        content_type="multipart/form-data",
        headers={"X-CSRFToken": "valid-csrf-token"}
    )
    assert res.status_code == 200
    json_data = res.get_json()
    assert json_data["success"] is True
    assert json_data["url"].startswith("/assets/uploads/test_avatar_")
    assert json_data["url"].endswith(".png")


def test_admin_dashboard_renders_with_tabs_and_data(logged_in_admin):
    res = logged_in_admin.get("/admin/dashboard")
    assert res.status_code == 200
    assert b"Inquiries &amp; Leads" in res.data
    assert b"Our People &amp; Mentors" in res.data
    assert b"Website Content &amp; Photos" in res.data
    assert b"Modify Enquired Person" in res.data
    assert b"Add Inquired Person" in res.data
