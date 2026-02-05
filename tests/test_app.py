"""Tests for the Mergington High School API."""
import pytest


class TestGetActivities:
    """Test the GET /activities endpoint."""

    def test_get_activities_returns_all_activities(self, test_client):
        """Test that get_activities returns all activities."""
        response = test_client.get("/activities")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, dict)
        assert "Chess Club" in data
        assert "Programming Class" in data
        assert "Gym Class" in data
        assert "Basketball Club" in data

    def test_get_activities_returns_activity_details(self, test_client):
        """Test that each activity contains required fields."""
        response = test_client.get("/activities")
        data = response.json()
        
        activity = data["Chess Club"]
        assert "description" in activity
        assert "schedule" in activity
        assert "max_participants" in activity
        assert "participants" in activity
        assert isinstance(activity["participants"], list)

    def test_get_activities_shows_current_participants(self, test_client):
        """Test that get_activities shows current participants."""
        response = test_client.get("/activities")
        data = response.json()
        
        chess_participants = data["Chess Club"]["participants"]
        assert "michael@mergington.edu" in chess_participants
        assert "daniel@mergington.edu" in chess_participants


class TestSignupForActivity:
    """Test the POST /activities/{activity_name}/signup endpoint."""

    def test_signup_for_activity_success(self, test_client):
        """Test successful signup for an activity."""
        response = test_client.post(
            "/activities/Chess%20Club/signup?email=newstudent@mergington.edu"
        )
        assert response.status_code == 200
        assert "Signed up" in response.json()["message"]

    def test_signup_adds_participant_to_activity(self, test_client):
        """Test that signup actually adds participant to activity."""
        test_client.post(
            "/activities/Chess%20Club/signup?email=newstudent@mergington.edu"
        )
        
        response = test_client.get("/activities")
        data = response.json()
        assert "newstudent@mergington.edu" in data["Chess Club"]["participants"]

    def test_signup_for_nonexistent_activity_returns_404(self, test_client):
        """Test that signup for nonexistent activity returns 404."""
        response = test_client.post(
            "/activities/Nonexistent%20Club/signup?email=newstudent@mergington.edu"
        )
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_signup_duplicate_student_returns_400(self, test_client):
        """Test that signup fails if student is already registered."""
        response = test_client.post(
            "/activities/Chess%20Club/signup?email=michael@mergington.edu"
        )
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"].lower()

    def test_signup_multiple_activities(self, test_client):
        """Test that a student can sign up for multiple activities."""
        student_email = "versatile@mergington.edu"
        
        # Sign up for Chess Club
        response1 = test_client.post(
            f"/activities/Chess%20Club/signup?email={student_email}"
        )
        assert response1.status_code == 200
        
        # Sign up for Programming Class
        response2 = test_client.post(
            f"/activities/Programming%20Class/signup?email={student_email}"
        )
        assert response2.status_code == 200
        
        # Verify both signups
        response = test_client.get("/activities")
        data = response.json()
        assert student_email in data["Chess Club"]["participants"]
        assert student_email in data["Programming Class"]["participants"]


class TestUnregisterFromActivity:
    """Test the DELETE /activities/{activity_name}/unregister endpoint."""

    def test_unregister_success(self, test_client):
        """Test successful unregister from an activity."""
        response = test_client.delete(
            "/activities/Chess%20Club/unregister?email=michael@mergington.edu"
        )
        assert response.status_code == 200
        assert "Unregistered" in response.json()["message"]

    def test_unregister_removes_participant(self, test_client):
        """Test that unregister actually removes participant."""
        test_client.delete(
            "/activities/Chess%20Club/unregister?email=michael@mergington.edu"
        )
        
        response = test_client.get("/activities")
        data = response.json()
        assert "michael@mergington.edu" not in data["Chess Club"]["participants"]

    def test_unregister_from_nonexistent_activity_returns_404(self, test_client):
        """Test that unregister from nonexistent activity returns 404."""
        response = test_client.delete(
            "/activities/Nonexistent%20Club/unregister?email=student@mergington.edu"
        )
        assert response.status_code == 404

    def test_unregister_not_registered_student_returns_400(self, test_client):
        """Test that unregister fails for student not registered."""
        response = test_client.delete(
            "/activities/Chess%20Club/unregister?email=notregistered@mergington.edu"
        )
        assert response.status_code == 400
        assert "not signed up" in response.json()["detail"].lower()

    def test_signup_and_unregister_flow(self, test_client):
        """Test the complete signup and unregister flow."""
        student_email = "flowtest@mergington.edu"
        
        # Sign up
        response1 = test_client.post(
            f"/activities/Tennis%20Club/signup?email={student_email}"
        )
        assert response1.status_code == 200
        
        # Verify signup
        response = test_client.get("/activities")
        assert student_email in response.json()["Tennis Club"]["participants"]
        
        # Unregister
        response2 = test_client.delete(
            f"/activities/Tennis%20Club/unregister?email={student_email}"
        )
        assert response2.status_code == 200
        
        # Verify unregister
        response = test_client.get("/activities")
        assert student_email not in response.json()["Tennis Club"]["participants"]


class TestActivityIntegration:
    """Integration tests for activity management."""

    def test_participant_count_accuracy(self, test_client):
        """Test that participant count is accurate."""
        response = test_client.get("/activities")
        data = response.json()
        
        chess_participants = data["Chess Club"]["participants"]
        assert len(chess_participants) == 2
        
        # Add a participant
        test_client.post(
            "/activities/Chess%20Club/signup?email=newstudent@mergington.edu"
        )
        
        response = test_client.get("/activities")
        data = response.json()
        assert len(data["Chess Club"]["participants"]) == 3

    def test_max_participants_validation(self, test_client):
        """Test that we can sign up students up to max_participants."""
        response = test_client.get("/activities")
        data = response.json()
        
        # Tennis Club has max 10 and 1 current participant
        tennis = data["Tennis Club"]
        assert tennis["max_participants"] == 10
        assert len(tennis["participants"]) == 1
        available_spots = tennis["max_participants"] - len(tennis["participants"])
        assert available_spots == 9
