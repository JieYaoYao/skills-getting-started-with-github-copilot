from src import app as app_module


def test_get_activities_returns_all_activities(client):
    # Arrange
    expected_keys = set(app_module.activities.keys())

    # Act
    resp = client.get("/activities")

    # Assert
    assert resp.status_code == 200
    data = resp.json()
    assert set(data.keys()) == expected_keys


def test_signup_for_activity_adds_participant(client):
    # Arrange
    activity = "Chess Club"
    email = "newstudent@mergington.edu"
    assert email not in app_module.activities[activity]["participants"]

    # Act
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert resp.status_code == 200
    assert email in app_module.activities[activity]["participants"]


def test_signup_for_activity_duplicate_returns_400(client):
    # Arrange
    activity = "Chess Club"
    email = "dupstudent@mergington.edu"
    # make sure participant exists
    client.post(f"/activities/{activity}/signup", params={"email": email})

    # Act
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert resp.status_code == 400


def test_signup_for_nonexistent_activity_returns_404(client):
    # Arrange
    activity = "No Such Activity"
    email = "a@b.test"

    # Act
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert resp.status_code == 404


def test_remove_participant_from_activity_removes_participant(client):
    # Arrange
    activity = "Programming Class"
    email = "toremove@mergington.edu"
    client.post(f"/activities/{activity}/signup", params={"email": email})
    assert email in app_module.activities[activity]["participants"]

    # Act
    resp = client.delete(f"/activities/{activity}/participants", params={"email": email})

    # Assert
    assert resp.status_code == 200
    assert email not in app_module.activities[activity]["participants"]


def test_remove_nonexistent_participant_returns_404(client):
    # Arrange
    activity = "Programming Class"
    email = "doesnotexist@mergington.edu"
    assert email not in app_module.activities[activity]["participants"]

    # Act
    resp = client.delete(f"/activities/{activity}/participants", params={"email": email})

    # Assert
    assert resp.status_code == 404
