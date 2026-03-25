"""
Tests for GET /activities endpoint.
"""

import pytest


class TestGetActivities:
    """Tests for fetching all activities."""

    def test_get_activities_success(self, mock_app):
        """Test successful fetch of all activities returns 200."""
        response = mock_app.get("/activities")
        assert response.status_code == 200

    def test_get_activities_returns_dict(self, mock_app):
        """Test that GET /activities returns a dictionary (not a list)."""
        response = mock_app.get("/activities")
        data = response.json()
        assert isinstance(data, dict)

    def test_get_activities_contains_all_activities(self, mock_app, activities_data):
        """Test that all expected activities are present in the response."""
        response = mock_app.get("/activities")
        activities = response.json()
        
        for activity_name in activities_data.keys():
            assert activity_name in activities

    def test_get_activities_response_structure(self, mock_app):
        """Test that each activity has the required fields."""
        response = mock_app.get("/activities")
        activities = response.json()
        
        required_fields = {"description", "schedule", "max_participants", "participants"}
        
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_data, dict), f"{activity_name} should be a dict"
            assert required_fields.issubset(activity_data.keys()), \
                f"{activity_name} missing required fields"

    def test_get_activities_field_types(self, mock_app):
        """Test that activity fields have correct types."""
        response = mock_app.get("/activities")
        activities = response.json()
        
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_data["description"], str), \
                f"{activity_name} description should be string"
            assert isinstance(activity_data["schedule"], str), \
                f"{activity_name} schedule should be string"
            assert isinstance(activity_data["max_participants"], int), \
                f"{activity_name} max_participants should be int"
            assert isinstance(activity_data["participants"], list), \
                f"{activity_name} participants should be list"

    def test_get_activities_initial_participants(self, mock_app, activities_data):
        """Test that initial participant lists match expected data."""
        response = mock_app.get("/activities")
        activities = response.json()
        
        for activity_name, expected_activity in activities_data.items():
            actual_participants = activities[activity_name]["participants"]
            expected_participants = expected_activity["participants"]
            assert actual_participants == expected_participants, \
                f"{activity_name} participants don't match"

    def test_get_activities_max_participants_values(self, mock_app, activities_data):
        """Test that max_participants values are correct."""
        response = mock_app.get("/activities")
        activities = response.json()
        
        for activity_name, expected_activity in activities_data.items():
            actual_max = activities[activity_name]["max_participants"]
            expected_max = expected_activity["max_participants"]
            assert actual_max == expected_max, \
                f"{activity_name} max_participants mismatch"

    @pytest.mark.parametrize("activity_name", [
        "Chess Club",
        "Programming Class",
        "Gym Class",
        "Basketball Team",
        "Soccer Club",
        "Art Studio",
        "Drama Club",
        "Debate Team",
        "Science Club"
    ])
    def test_get_activities_each_activity_present(self, mock_app, activity_name):
        """Test each specific activity is present in the response."""
        response = mock_app.get("/activities")
        activities = response.json()
        assert activity_name in activities
