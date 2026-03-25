"""
Tests for POST /activities/{activity_name}/signup endpoint.
"""

import pytest


class TestPostSignup:
    """Tests for signing up a student for an activity."""

    # Successful signup tests
    def test_signup_success(self, mock_app):
        """Test successful signup returns 200 and correct message."""
        response = mock_app.post(
            "/activities/Chess Club/signup?email=newstudent@mergington.edu"
        )
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "Signed up" in data["message"]
        assert "newstudent@mergington.edu" in data["message"]
        assert "Chess Club" in data["message"]

    def test_signup_adds_participant(self, mock_app):
        """Test that signup actually adds the email to participants list."""
        email = "newstudent@mergington.edu"
        
        # Verify email not in participants initially
        response = mock_app.get("/activities")
        activities = response.json()
        chess_participants = activities["Chess Club"]["participants"]
        assert email not in chess_participants
        
        # Perform signup
        response = mock_app.post(f"/activities/Chess Club/signup?email={email}")
        assert response.status_code == 200
        
        # Verify email now in participants
        response = mock_app.get("/activities")
        activities = response.json()
        chess_participants = activities["Chess Club"]["participants"]
        assert email in chess_participants

    def test_signup_multiple_participants(self, mock_app):
        """Test that multiple signups add all emails to participants."""
        emails = ["user1@school.edu", "user2@school.edu", "user3@school.edu"]
        activity = "Programming Class"
        
        for email in emails:
            response = mock_app.post(f"/activities/{activity}/signup?email={email}")
            assert response.status_code == 200
        
        # Verify all emails in participants
        response = mock_app.get("/activities")
        activities = response.json()
        participants = activities[activity]["participants"]
        
        for email in emails:
            assert email in participants

    def test_signup_different_activities(self, mock_app):
        """Test that signup to different activities works independently."""
        email = "student@school.edu"
        
        # Signup to two different activities
        response1 = mock_app.post(f"/activities/Chess Club/signup?email={email}")
        response2 = mock_app.post(f"/activities/Drama Club/signup?email={email}")
        
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        # Verify in both activities
        response = mock_app.get("/activities")
        activities = response.json()
        assert email in activities["Chess Club"]["participants"]
        assert email in activities["Drama Club"]["participants"]

    # Activity not found tests
    def test_signup_activity_not_found(self, mock_app):
        """Test signup to non-existent activity returns 404."""
        response = mock_app.post(
            "/activities/Nonexistent Club/signup?email=student@school.edu"
        )
        assert response.status_code == 404
        data = response.json()
        assert "Activity not found" in data["detail"]

    # Duplicate signup tests
    def test_signup_duplicate_email_same_activity(self, mock_app):
        """Test that signing up same email twice returns 400."""
        email = "student@school.edu"
        activity = "Chess Club"
        
        # First signup should succeed
        response1 = mock_app.post(f"/activities/{activity}/signup?email={email}")
        assert response1.status_code == 200
        
        # Second signup with same email should fail
        response2 = mock_app.post(f"/activities/{activity}/signup?email={email}")
        assert response2.status_code == 400
        data = response2.json()
        assert "already signed up" in data["detail"]

    def test_signup_duplicate_does_not_add_participant(self, mock_app):
        """Test that duplicate signup attempt doesn't modify participants list."""
        email = "student@school.edu"
        activity = "Chess Club"
        
        # First signup
        mock_app.post(f"/activities/{activity}/signup?email={email}")
        response = mock_app.get("/activities")
        activities = response.json()
        count_after_first = activities[activity]["participants"].count(email)
        
        # Second signup attempt
        mock_app.post(f"/activities/{activity}/signup?email={email}")
        response = mock_app.get("/activities")
        activities = response.json()
        count_after_second = activities[activity]["participants"].count(email)
        
        # Should still be 1, not 2
        assert count_after_first == 1
        assert count_after_second == 1

    # Parametrized tests
    @pytest.mark.parametrize("email", [
        "alice@mergington.edu",
        "bob.smith@mergington.edu",
        "charlie_2024@mergington.edu",
        "diana.test@mergington.edu",
    ])
    def test_signup_various_email_formats(self, mock_app, email):
        """Test signup works with various email formats."""
        response = mock_app.post(f"/activities/Art Studio/signup?email={email}")
        assert response.status_code == 200
        
        # Verify email added
        response = mock_app.get("/activities")
        activities = response.json()
        assert email in activities["Art Studio"]["participants"]

    @pytest.mark.parametrize("activity_name", [
        "Chess Club",
        "Programming Class",
        "Basketball Team",
        "Science Club",
    ])
    def test_signup_to_various_activities(self, mock_app, activity_name):
        """Test signup works for various activities."""
        email = "testuser@school.edu"
        response = mock_app.post(f"/activities/{activity_name}/signup?email={email}")
        assert response.status_code == 200
        
        # Verify added
        response = mock_app.get("/activities")
        activities = response.json()
        assert email in activities[activity_name]["participants"]

    # Edge case tests
    def test_signup_first_to_empty_activity(self, mock_app):
        """Test signup when activity has no participants initially."""
        # Find an activity with no participants
        response = mock_app.get("/activities")
        activities = response.json()
        
        empty_activity = None
        for name, details in activities.items():
            if not details["participants"]:
                empty_activity = name
                break
        
        if empty_activity:
            email = "firstuser@school.edu"
            response = mock_app.post(f"/activities/{empty_activity}/signup?email={email}")
            assert response.status_code == 200
            
            response = mock_app.get("/activities")
            activities = response.json()
            assert email in activities[empty_activity]["participants"]
            assert len(activities[empty_activity]["participants"]) == 1

    def test_signup_existing_initial_participant(self, mock_app):
        """Test that initial participants from app.py are present."""
        response = mock_app.get("/activities")
        activities = response.json()
        
        # Chess Club initially has michael@mergington.edu
        assert "michael@mergington.edu" in activities["Chess Club"]["participants"]
        assert "daniel@mergington.edu" in activities["Chess Club"]["participants"]

    def test_signup_response_content_type(self, mock_app):
        """Test that response has proper JSON content type."""
        response = mock_app.post(
            "/activities/Soccer Club/signup?email=tester@school.edu"
        )
        assert response.headers["content-type"] == "application/json"
