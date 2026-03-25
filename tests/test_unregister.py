"""
Tests for DELETE /activities/{activity_name}/signup endpoint.
"""

import pytest


class TestDeleteUnregister:
    """Tests for unregistering a student from an activity."""

    # Successful unregister tests
    def test_unregister_success(self, mock_app):
        """Test successful unregister returns 200 and correct message."""
        email = "michael@mergington.edu"
        activity = "Chess Club"
        
        response = mock_app.delete(
            f"/activities/{activity}/signup?email={email}"
        )
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "Unregistered" in data["message"]
        assert email in data["message"]
        assert activity in data["message"]

    def test_unregister_removes_participant(self, mock_app):
        """Test that unregister actually removes the email from participants list."""
        email = "michael@mergington.edu"
        activity = "Chess Club"
        
        # Verify email in participants initially
        response = mock_app.get("/activities")
        activities = response.json()
        assert email in activities[activity]["participants"]
        
        # Perform unregister
        response = mock_app.delete(f"/activities/{activity}/signup?email={email}")
        assert response.status_code == 200
        
        # Verify email no longer in participants
        response = mock_app.get("/activities")
        activities = response.json()
        assert email not in activities[activity]["participants"]

    def test_unregister_preserves_other_participants(self, mock_app):
        """Test that unregister only removes the target email, not others."""
        activity = "Chess Club"
        email_to_remove = "michael@mergington.edu"
        other_email = "daniel@mergington.edu"
        
        # Perform unregister
        response = mock_app.delete(f"/activities/{activity}/signup?email={email_to_remove}")
        assert response.status_code == 200
        
        # Verify other participant still present
        response = mock_app.get("/activities")
        activities = response.json()
        assert email_to_remove not in activities[activity]["participants"]
        assert other_email in activities[activity]["participants"]

    def test_unregister_multiple_participants(self, mock_app):
        """Test unregistering multiple participants sequentially."""
        activity = "Drama Club"
        
        # Drama Club has noah@mergington.edu and mia@mergington.edu
        emails = ["noah@mergington.edu", "mia@mergington.edu"]
        
        for email in emails:
            response = mock_app.delete(f"/activities/{activity}/signup?email={email}")
            assert response.status_code == 200
        
        # Verify both removed
        response = mock_app.get("/activities")
        activities = response.json()
        for email in emails:
            assert email not in activities[activity]["participants"]

    def test_unregister_last_participant(self, mock_app):
        """Test unregistering the last participant from an activity."""
        activity = "Art Studio"
        email = "ava@mergington.edu"  # Art Studio's only participant
        
        # Verify it's the last one
        response = mock_app.get("/activities")
        activities = response.json()
        assert len(activities[activity]["participants"]) == 1
        
        # Unregister
        response = mock_app.delete(f"/activities/{activity}/signup?email={email}")
        assert response.status_code == 200
        
        # Verify activity now has no participants
        response = mock_app.get("/activities")
        activities = response.json()
        assert len(activities[activity]["participants"]) == 0

    # Activity not found tests
    def test_unregister_activity_not_found(self, mock_app):
        """Test unregister from non-existent activity returns 404."""
        response = mock_app.delete(
            "/activities/Nonexistent Club/signup?email=student@school.edu"
        )
        assert response.status_code == 404
        data = response.json()
        assert "Activity not found" in data["detail"]

    # Student not enrolled tests
    def test_unregister_student_not_enrolled(self, mock_app):
        """Test unregister of non-enrolled student returns 400."""
        email = "notenrolled@school.edu"
        activity = "Chess Club"
        
        response = mock_app.delete(f"/activities/{activity}/signup?email={email}")
        assert response.status_code == 400
        data = response.json()
        assert "not signed up" in data["detail"]

    def test_unregister_already_unregistered(self, mock_app):
        """Test unregistering someone who was already unregistered returns 400."""
        email = "michael@mergington.edu"
        activity = "Chess Club"
        
        # First unregister should succeed
        response1 = mock_app.delete(f"/activities/{activity}/signup?email={email}")
        assert response1.status_code == 200
        
        # Second unregister should fail
        response2 = mock_app.delete(f"/activities/{activity}/signup?email={email}")
        assert response2.status_code == 400
        data = response2.json()
        assert "not signed up" in data["detail"]

    def test_unregister_does_not_affect_other_activity(self, mock_app):
        """Test that unregistering from one activity doesn't affect others."""
        email = "lucas@mergington.edu"  # In Soccer Club
        activity_to_leave = "Soccer Club"
        activity_to_stay = "Soccer Club"  # Same activity for this test
        
        # Signup to Drama Club
        mock_app.post("/activities/Drama Club/signup?email=lucas@mergington.edu")
        
        # Unregister from Soccer Club
        mock_app.delete(f"/activities/{activity_to_leave}/signup?email={email}")
        
        # Verify still in Drama Club
        response = mock_app.get("/activities")
        activities = response.json()
        assert email in activities["Drama Club"]["participants"]

    # Parametrized tests
    @pytest.mark.parametrize("email,activity", [
        ("michael@mergington.edu", "Chess Club"),
        ("emma@mergington.edu", "Programming Class"),
        ("john@mergington.edu", "Gym Class"),
        ("grace@mergington.edu", "Debate Team"),
    ])
    def test_unregister_various_initial_participants(self, mock_app, email, activity):
        """Test unregistering various initial participants."""
        response = mock_app.delete(f"/activities/{activity}/signup?email={email}")
        assert response.status_code == 200
        
        # Verify removed
        response = mock_app.get("/activities")
        activities = response.json()
        assert email not in activities[activity]["participants"]

    # Integration tests: signup then unregister
    def test_signup_then_unregister_success(self, mock_app):
        """Test signup followed by unregister works correctly."""
        email = "newtester@school.edu"
        activity = "Science Club"
        
        # Signup
        response = mock_app.post(f"/activities/{activity}/signup?email={email}")
        assert response.status_code == 200
        
        # Verify added
        response = mock_app.get("/activities")
        activities = response.json()
        assert email in activities[activity]["participants"]
        
        # Unregister
        response = mock_app.delete(f"/activities/{activity}/signup?email={email}")
        assert response.status_code == 200
        
        # Verify removed
        response = mock_app.get("/activities")
        activities = response.json()
        assert email not in activities[activity]["participants"]

    def test_signup_unregister_unregister_fails(self, mock_app):
        """Test that unregistering twice fails appropriately."""
        email = "tester@school.edu"
        activity = "Art Studio"
        
        # Signup
        mock_app.post(f"/activities/{activity}/signup?email={email}")
        
        # First unregister should succeed
        response1 = mock_app.delete(f"/activities/{activity}/signup?email={email}")
        assert response1.status_code == 200
        
        # Second unregister should fail
        response2 = mock_app.delete(f"/activities/{activity}/signup?email={email}")
        assert response2.status_code == 400
        data = response2.json()
        assert "not signed up" in data["detail"]

    # Edge cases
    def test_unregister_response_content_type(self, mock_app):
        """Test that response has proper JSON content type."""
        response = mock_app.delete(
            "/activities/Chess Club/signup?email=michael@mergington.edu"
        )
        assert response.headers["content-type"] == "application/json"
