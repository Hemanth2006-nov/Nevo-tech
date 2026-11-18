import sqlite3

import pytest

import server


@pytest.fixture
def client(monkeypatch):
    server.app.config.update(TESTING=True)
    monkeypatch.setattr(server, "_verify_turnstile", lambda _token: True)
    return server.app.test_client()


def valid_enquiry(**overrides):
    data = {
        "fullName": "Test Customer",
        "email": "customer@example.com",
        "phone": "+91 98765 43210",
        "service": "Technical Internship Programs",
        "institution": "Test University",
        "domain": "Software Engineering",
        "message": "Please share more information.",
    }
    data.update(overrides)
    return data


def test_invalid_enquiry_is_rejected_without_database_write(client, monkeypatch):
    def unexpected_insert(_data):
        pytest.fail("Invalid enquiry should not be persisted")

    monkeypatch.setattr(server.db, "insert_enquiry", unexpected_insert)
    response = client.post(
        "/api/enquiries",
        json=valid_enquiry(email="invalid"),
        environ_base={"REMOTE_ADDR": "192.0.2.10"},
    )

    assert response.status_code == 400
    assert response.get_json()["success"] is False


def test_honeypot_submission_is_not_persisted(client, monkeypatch):
    def unexpected_insert(_data):
        pytest.fail("Honeypot submissions should not be persisted")

    monkeypatch.setattr(server.db, "insert_enquiry", unexpected_insert)
    response = client.post(
        "/api/enquiries",
        json=valid_enquiry(website="automated spam"),
        environ_base={"REMOTE_ADDR": "192.0.2.11"},
    )

    assert response.status_code == 202
    assert response.get_json()["success"] is True


def test_valid_enquiry_is_saved_before_success_is_returned(client, monkeypatch):
    saved_data = {}

    def insert(data):
        saved_data.update(data)
        return {"id": 42, "created_at": "2026-01-01T00:00:00"}

    monkeypatch.setattr(server.db, "insert_enquiry", insert)
    monkeypatch.setattr(server, "_send_notifications", lambda _data, _id: None)
    response = client.post(
        "/api/enquiries",
        json=valid_enquiry(),
        environ_base={"REMOTE_ADDR": "192.0.2.12"},
    )

    assert response.status_code == 201
    assert response.get_json()["data"]["id"] == 42
    assert saved_data["email"] == "customer@example.com"


def test_database_failure_does_not_return_success(client, monkeypatch):
    def failed_insert(_data):
        raise RuntimeError("simulated storage failure")

    monkeypatch.setattr(server.db, "insert_enquiry", failed_insert)
    response = client.post(
        "/api/enquiries",
        json=valid_enquiry(),
        environ_base={"REMOTE_ADDR": "192.0.2.13"},
    )

    assert response.status_code == 503
    assert response.get_json()["success"] is False


def test_new_enquiry_is_recorded_in_audit_log(tmp_path, monkeypatch):
    database_path = tmp_path / "audit-test.db"
    monkeypatch.setattr(server.db, "SQLITE_PATH", str(database_path))
    monkeypatch.setattr(server.db, "IS_POSTGRES", False)
    server.db.init_db()
    server.db.insert_enquiry(valid_enquiry())

    with sqlite3.connect(database_path) as connection:
        audit_action = connection.execute(
            "SELECT action FROM admin_audit_log WHERE action = 'enquiry_created'"
        ).fetchone()

    assert audit_action == ("enquiry_created",)


def test_admin_mutation_requires_csrf_token(client, monkeypatch):
    monkeypatch.setattr(server.db, "update_enquiry_status", lambda *_args: True)
    with client.session_transaction() as current_session:
        current_session["is_admin"] = True
        current_session["_csrf_token"] = "test-csrf-token"

    rejected = client.patch("/api/enquiries/1", json={"status": "Contacted"})
    accepted = client.patch(
        "/api/enquiries/1",
        json={"status": "Contacted"},
        headers={"X-CSRFToken": "test-csrf-token"},
    )

    assert rejected.status_code == 403
    assert accepted.status_code == 200


def test_admin_login_reports_missing_local_configuration(client, monkeypatch):
    monkeypatch.setattr(server, "ADMIN_AUTH_CONFIGURED", False)
    response = client.get("/admin/login")

    assert response.status_code == 503
    assert b"Admin login is not configured" in response.data


def test_admin_login_requires_the_configured_username_and_password(client, monkeypatch):
    monkeypatch.setattr(server, "ADMIN_AUTH_CONFIGURED", True)
    monkeypatch.setattr(server, "ADMIN_USERNAME", "nevo-admin")
    monkeypatch.setattr(
        server,
        "_admin_password_matches",
        lambda candidate: candidate == "strong-test-password",
    )
    monkeypatch.setattr(server.db, "record_audit_event", lambda *_args: None)
    with client.session_transaction() as current_session:
        current_session["_csrf_token"] = "test-csrf-token"

    rejected = client.post(
        "/admin/login",
        data={
            "csrf_token": "test-csrf-token",
            "username": "wrong-user",
            "password": "strong-test-password",
        },
    )
    accepted = client.post(
        "/admin/login",
        data={
            "csrf_token": "test-csrf-token",
            "username": "nevo-admin",
            "password": "strong-test-password",
        },
    )

    assert rejected.status_code == 200
    assert b"Invalid administrator username or password" in rejected.data
    assert accepted.status_code == 302
    with client.session_transaction() as current_session:
        assert current_session["is_admin"] is True


def test_csv_export_requires_csrf_token(client, monkeypatch):
    monkeypatch.setattr(server.db, "record_audit_event", lambda *_args: None)
    monkeypatch.setattr(server.db, "get_all_enquiries", lambda: [])
    with client.session_transaction() as current_session:
        current_session["is_admin"] = True
        current_session["_csrf_token"] = "test-csrf-token"

    rejected = client.post("/admin/export-csv")
    accepted = client.post(
        "/admin/export-csv",
        data={"csrf_token": "test-csrf-token"},
    )

    assert rejected.status_code == 403
    assert accepted.status_code == 200
    assert accepted.mimetype == "text/csv"


def test_unknown_and_private_files_return_404(client):
    assert client.get("/server.py").status_code == 404
    assert client.get("/not-a-real-page").status_code == 404
