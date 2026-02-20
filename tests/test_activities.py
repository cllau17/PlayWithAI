"""
Tests for activity-related endpoints.
Tests follow the AAA (Arrange-Act-Assert) pattern.
"""

import pytest


class TestGetActivities:
    """Tests for GET /activities endpoint."""
    
    def test_get_all_activities_returns_correct_count(self, client):
        """After getting activities, should return all 9 activities."""
        # Arrange (setup already done by reset_activities fixture)
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        assert len(activities) == 9
        assert response.status_code == 200
    
    def test_get_all_activities_returns_valid_structure(self, client):
        """Activity objects should have required fields."""
        # Arrange
        expected_fields = {"description", "schedule", "max_participants", "participants"}
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        assert response.status_code == 200
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_name, str)
            assert isinstance(activity_data, dict)
            assert expected_fields.issubset(activity_data.keys())
    
    def test_get_all_activities_includes_participant_lists(self, client):
        """Activities should include participants list."""
        # Arrange
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        assert response.status_code == 200
        chess_club = activities.get("Chess Club")
        assert chess_club is not None
        assert "participants" in chess_club
        assert isinstance(chess_club["participants"], list)
        assert len(chess_club["participants"]) == 2
        assert "michael@mergington.edu" in chess_club["participants"]
    
    def test_get_all_activities_participant_count_matches_max(self, client):
        """Participants should not exceed max_participants."""
        # Arrange
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        assert response.status_code == 200
        for activity_name, activity_data in activities.items():
            assert len(activity_data["participants"]) <= activity_data["max_participants"]
    
    def test_get_all_activities_response_is_json(self, client):
        """Response should be valid JSON."""
        # Arrange
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"
        assert isinstance(response.json(), dict)


class TestRootRedirect:
    """Tests for GET / endpoint."""
    
    def test_root_redirects_to_index(self, client):
        """GET / should redirect to /static/index.html."""
        # Arrange
        
        # Act
        response = client.get("/", follow_redirects=False)
        
        # Assert
        assert response.status_code == 307
        assert "location" in response.headers
        assert response.headers["location"] == "/static/index.html"
    
    def test_root_redirect_follows_to_index(self, client):
        """GET / with follow_redirects should reach index.html."""
        # Arrange
        
        # Act
        response = client.get("/", follow_redirects=True)
        
        # Assert
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
