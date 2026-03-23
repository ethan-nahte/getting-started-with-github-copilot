def test_get_activities_returns_200(client):
    # Arrange - client fixture provides TestClient
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200


def test_get_activities_returns_all_activities(client):
    # Arrange
    
    # Act
    response = client.get("/activities")
    
    # Assert
    data = response.json()
    assert len(data) == 9
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_get_activities_has_required_fields(client):
    # Arrange
    
    # Act
    response = client.get("/activities")
    
    # Assert
    data = response.json()
    activity = data["Chess Club"]
    assert "description" in activity
    assert "schedule" in activity
    assert "max_participants" in activity
    assert "participants" in activity
    assert isinstance(activity["participants"], list)


def test_signup_success(client):
    # Arrange
    
    # Act
    response = client.post("/activities/Chess Club/signup?email=newstudent@mergington.edu")
    
    # Assert
    assert response.status_code == 200
    assert "Signed up newstudent@mergington.edu for Chess Club" in response.json()["message"]


def test_signup_duplicate_returns_400(client):
    # Arrange - michael@mergington.edu already in Chess Club
    
    # Act
    response = client.post("/activities/Chess Club/signup?email=michael@mergington.edu")
    
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_invalid_activity_returns_404(client):
    # Arrange
    
    # Act
    response = client.post("/activities/NonExistent/signup?email=test@mergington.edu")
    
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_signup_at_capacity_returns_400(client):
    # Arrange - Fill Chess Club to capacity (max 12, currently 2)
    for i in range(10):
        client.post(f"/activities/Chess Club/signup?email=student{i}@mergington.edu")
    
    # Act - Try to signup 11th student
    response = client.post("/activities/Chess Club/signup?email=overflow@mergington.edu")
    
    # Assert
    assert response.status_code == 400
    assert "at full capacity" in response.json()["detail"]


def test_unregister_success(client):
    # Arrange
    
    # Act
    response = client.delete("/activities/Chess Club/unregister?email=michael@mergington.edu")
    
    # Assert
    assert response.status_code == 200
    assert "Unregistered michael@mergington.edu from Chess Club" in response.json()["message"]


def test_unregister_not_enrolled_returns_400(client):
    # Arrange
    
    # Act
    response = client.delete("/activities/Chess Club/unregister?email=notenrolled@mergington.edu")
    
    # Assert
    assert response.status_code == 400
    assert "not signed up" in response.json()["detail"]


def test_unregister_invalid_activity_returns_404(client):
    # Arrange
    
    # Act
    response = client.delete("/activities/NonExistent/unregister?email=test@mergington.edu")
    
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_signup_case_sensitive_activity_name(client):
    # Arrange
    
    # Act
    response = client.post("/activities/chess club/signup?email=test@mergington.edu")
    
    # Assert
    assert response.status_code == 404  # Case sensitive, should not find


def test_signup_empty_email(client):
    # Arrange
    
    # Act
    response = client.post("/activities/Chess Club/signup?email=")
    
    # Assert
    assert response.status_code == 200  # Currently allows empty, but maybe should validate
    # Note: Email validation could be added later
