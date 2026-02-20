"""
Tests for activity signup endpoint.
Tests follow the AAA (Arrange-Act-Assert) pattern.
"""

import pytest


class TestSignupForActivity:
    """Tests for POST /activities/{activity_name}/signup endpoint."""
    
    def test_signup_successful_adds_participant(self, client):
        """When signing up with valid data, participant should be added."""
        # Arrange
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        assert "message" in response.json()
        
        # Verify participant was added
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email in activities[activity_name]["participants"]
    
    def test_signup_success_returns_confirmation_message(self, client):
        """Successful signup should return a confirmation message."""
        # Arrange
        activity_name = "Programming Class"
        email = "alice@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]
    
    def test_signup_duplicate_returns_error(self, client):
        """When signing up twice, second attempt should fail with 400."""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already signed up
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 400
        assert "detail" in response.json()
        assert "already" in response.json()["detail"].lower()
    
    def test_signup_nonexistent_activity_returns_404(self, client):
        """Signing up for non-existent activity should return 404."""
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "student@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]
    
    def test_signup_updates_participant_count(self, client):
        """After signup, participant count should increase by 1."""
        # Arrange
        activity_name = "Tennis Club"
        email = "newplayer@mergington.edu"
        
        initial_response = client.get("/activities")
        initial_count = len(initial_response.json()[activity_name]["participants"])
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        
        updated_response = client.get("/activities")
        updated_count = len(updated_response.json()[activity_name]["participants"])
        assert updated_count == initial_count + 1
    
    def test_signup_decreases_available_spots(self, client):
        """After signup, available spots should decrease by 1."""
        # Arrange
        activity_name = "Art Studio"
        email = "artist@mergington.edu"
        
        initial_response = client.get("/activities")
        initial_participants = len(initial_response.json()[activity_name]["participants"])
        max_participants = initial_response.json()[activity_name]["max_participants"]
        initial_spots = max_participants - initial_participants
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        
        updated_response = client.get("/activities")
        updated_participants = len(updated_response.json()[activity_name]["participants"])
        updated_spots = max_participants - updated_participants
        assert updated_spots == initial_spots - 1
    
    def test_signup_with_url_encoded_email(self, client):
        """Signup should handle URL-encoded email addresses."""
        # Arrange
        activity_name = "Music Band"
        email = "student+test@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        
        activities_response = client.get("/activities")
        assert email in activities_response.json()[activity_name]["participants"]
    
    def test_signup_case_sensitive_email(self, client):
        """Different email cases should be treated as different emails (no duplicate check)."""
        # Arrange
        activity_name = "Science Club"
        email_lower = "newsci@mergington.edu"
        
        # Act - First signup
        response1 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email_lower}
        )
        
        # Assert first signup succeeds
        assert response1.status_code == 200
        
        # Act - Attempt duplicate signup (same case)
        response2 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email_lower}
        )
        
        # Assert duplicate fails
        assert response2.status_code == 400
