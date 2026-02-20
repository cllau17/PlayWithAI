"""
Tests for participant management endpoints.
Tests follow the AAA (Arrange-Act-Assert) pattern.
"""

import pytest


class TestRemoveParticipant:
    """Tests for DELETE /activities/{activity_name}/participants/{email} endpoint."""
    
    def test_remove_participant_successful(self, client):
        """When removing existing participant, should return success."""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Known participant
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )
        
        # Assert
        assert response.status_code == 200
        assert "message" in response.json()
    
    def test_remove_participant_deletes_from_list(self, client):
        """Removing participant should remove them from activity's participant list."""
        # Arrange
        activity_name = "Chess Club"
        email = "daniel@mergington.edu"
        
        # Verify they're in the list
        initial_response = client.get("/activities")
        assert email in initial_response.json()[activity_name]["participants"]
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )
        
        # Assert
        assert response.status_code == 200
        
        updated_response = client.get("/activities")
        assert email not in updated_response.json()[activity_name]["participants"]
    
    def test_remove_participant_decreases_count(self, client):
        """Removing participant should decrease participant count by 1."""
        # Arrange
        activity_name = "Programming Class"
        email = "emma@mergington.edu"
        
        initial_response = client.get("/activities")
        initial_count = len(initial_response.json()[activity_name]["participants"])
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )
        
        # Assert
        assert response.status_code == 200
        
        updated_response = client.get("/activities")
        updated_count = len(updated_response.json()[activity_name]["participants"])
        assert updated_count == initial_count - 1
    
    def test_remove_participant_increases_available_spots(self, client):
        """Removing participant should increase available spots by 1."""
        # Arrange
        activity_name = "Gym Class"
        email = "john@mergington.edu"
        
        initial_response = client.get("/activities")
        activity = initial_response.json()[activity_name]
        initial_spots = activity["max_participants"] - len(activity["participants"])
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )
        
        # Assert
        assert response.status_code == 200
        
        updated_response = client.get("/activities")
        updated_activity = updated_response.json()[activity_name]
        updated_spots = updated_activity["max_participants"] - len(updated_activity["participants"])
        assert updated_spots == initial_spots + 1
    
    def test_remove_nonexistent_participant_returns_404(self, client):
        """Removing non-existent participant should return 404."""
        # Arrange
        activity_name = "Basketball Team"
        email = "noone@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )
        
        # Assert
        assert response.status_code == 404
        assert "Participant not found" in response.json()["detail"]
    
    def test_remove_from_nonexistent_activity_returns_404(self, client):
        """Removing participant from non-existent activity should return 404."""
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "student@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )
        
        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]
    
    def test_remove_participant_does_not_affect_others(self, client):
        """Removing one participant should not affect others in same activity."""
        # Arrange
        activity_name = "Tennis Club"
        email_to_remove = "kevin@mergington.edu"
        email_to_keep = "lisa@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{email_to_remove}"
        )
        
        # Assert
        assert response.status_code == 200
        
        updated_response = client.get("/activities")
        participants = updated_response.json()[activity_name]["participants"]
        assert email_to_remove not in participants
        assert email_to_keep in participants
    
    def test_remove_participant_does_not_affect_other_activities(self, client):
        """Removing from one activity should not affect other activities."""
        # Arrange
        activity_to_modify = "Music Band"
        email_to_remove = "ryan@mergington.edu"
        other_activity = "Science Club"
        other_participants = ["david@mergington.edu", "rachel@mergington.edu"]
        
        # Act
        response = client.delete(
            f"/activities/{activity_to_modify}/participants/{email_to_remove}"
        )
        
        # Assert
        assert response.status_code == 200
        
        updated_response = client.get("/activities")
        for email in other_participants:
            assert email in updated_response.json()[other_activity]["participants"]
    
    def test_remove_second_participant_from_activity(self, client):
        """Should be able to remove participants until list is empty."""
        # Arrange
        activity_name = "Basketball Team"
        email = "alex@mergington.edu"  # Only participant
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )
        
        # Assert
        assert response.status_code == 200
        
        updated_response = client.get("/activities")
        assert len(updated_response.json()[activity_name]["participants"]) == 0
    
    def test_remove_with_url_encoded_email(self, client):
        """Should handle URL-encoded email addresses in DELETE."""
        # Arrange
        activity_name = "Art Studio"
        email = "grace@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )
        
        # Assert
        assert response.status_code == 200
        
        updated_response = client.get("/activities")
        assert email not in updated_response.json()[activity_name]["participants"]
