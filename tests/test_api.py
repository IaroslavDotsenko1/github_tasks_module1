"""
Test suite for Mergington High School Activities API

This module contains comprehensive tests for all API endpoints including:
- GET /activities - retrieving all activities
- POST /activities/{activity_name}/signup - signing up for activities  
- DELETE /activities/{activity_name}/unregister - unregistering from activities
- Edge cases and error handling
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities
import copy


@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    return TestClient(app)


@pytest.fixture
def backup_activities():
    """Backup the original activities data and restore after each test"""
    original_activities = copy.deepcopy(activities)
    yield
    # Restore original activities after test
    activities.clear()
    activities.update(original_activities)


class TestGetActivities:
    """Test cases for GET /activities endpoint"""
    
    def test_get_activities_success(self, client, backup_activities):
        """Test successful retrieval of all activities"""
        response = client.get("/activities")
        
        assert response.status_code == 200
        data = response.json()
        
        # Check that we get a dictionary of activities
        assert isinstance(data, dict)
        assert len(data) > 0
        
        # Check structure of first activity
        first_activity = next(iter(data.values()))
        required_fields = ["description", "schedule", "max_participants", "participants"]
        for field in required_fields:
            assert field in first_activity
        
        # Check that participants is a list
        assert isinstance(first_activity["participants"], list)
        assert isinstance(first_activity["max_participants"], int)
    
    def test_get_activities_contains_expected_activities(self, client, backup_activities):
        """Test that response contains expected activities"""
        response = client.get("/activities")
        data = response.json()
        
        expected_activities = [
            "Chess Club", "Programming Class", "Gym Class", 
            "Basketball Team", "Soccer Team", "Drama Club",
            "Art Workshop", "Science Club", "Debate Team"
        ]
        
        for activity in expected_activities:
            assert activity in data


class TestSignupForActivity:
    """Test cases for POST /activities/{activity_name}/signup endpoint"""
    
    def test_signup_success(self, client, backup_activities):
        """Test successful signup for an activity"""
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"
        
        response = client.post(f"/activities/{activity_name}/signup?email={email}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == f"Signed up {email} for {activity_name}"
        
        # Verify the participant was actually added
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert email in activities_data[activity_name]["participants"]
    
    def test_signup_duplicate_participant(self, client, backup_activities):
        """Test signing up a participant who is already registered"""
        activity_name = "Chess Club"
        # Use an email that's already in the Chess Club
        existing_email = "michael@mergington.edu"
        
        response = client.post(f"/activities/{activity_name}/signup?email={existing_email}")
        
        assert response.status_code == 400
        data = response.json()
        assert data["detail"] == "Student is already signed up"
    
    def test_signup_nonexistent_activity(self, client, backup_activities):
        """Test signing up for a non-existent activity"""
        activity_name = "Nonexistent Club"
        email = "student@mergington.edu"
        
        response = client.post(f"/activities/{activity_name}/signup?email={email}")
        
        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "Activity not found"
    
    def test_signup_url_encoded_activity_name(self, client, backup_activities):
        """Test signup with URL-encoded activity name"""
        activity_name = "Programming Class"
        encoded_name = "Programming%20Class"
        email = "programmer@mergington.edu"
        
        response = client.post(f"/activities/{encoded_name}/signup?email={email}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == f"Signed up {email} for {activity_name}"
    
    def test_signup_special_characters_in_email(self, client, backup_activities):
        """Test signup with special characters in email"""
        import urllib.parse
        
        activity_name = "Chess Club"
        email = "student+test@mergington.edu"
        encoded_email = urllib.parse.quote(email)
        
        response = client.post(f"/activities/{activity_name}/signup?email={encoded_email}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == f"Signed up {email} for {activity_name}"


class TestUnregisterFromActivity:
    """Test cases for DELETE /activities/{activity_name}/unregister endpoint"""
    
    def test_unregister_success(self, client, backup_activities):
        """Test successful unregistration from an activity"""
        activity_name = "Chess Club"
        # Use an existing participant
        existing_email = "michael@mergington.edu"
        
        # Verify participant is initially registered
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert existing_email in activities_data[activity_name]["participants"]
        
        # Unregister the participant
        response = client.delete(f"/activities/{activity_name}/unregister?email={existing_email}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == f"Unregistered {existing_email} from {activity_name}"
        
        # Verify the participant was actually removed
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert existing_email not in activities_data[activity_name]["participants"]
    
    def test_unregister_nonexistent_participant(self, client, backup_activities):
        """Test unregistering a participant who is not registered"""
        activity_name = "Chess Club"
        email = "notregistered@mergington.edu"
        
        response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
        
        assert response.status_code == 400
        data = response.json()
        assert data["detail"] == "Student is not registered for this activity"
    
    def test_unregister_nonexistent_activity(self, client, backup_activities):
        """Test unregistering from a non-existent activity"""
        activity_name = "Nonexistent Club"
        email = "student@mergington.edu"
        
        response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
        
        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "Activity not found"
    
    def test_unregister_url_encoded_activity_name(self, client, backup_activities):
        """Test unregister with URL-encoded activity name"""
        activity_name = "Programming Class"
        encoded_name = "Programming%20Class"
        existing_email = "emma@mergington.edu"
        
        response = client.delete(f"/activities/{encoded_name}/unregister?email={existing_email}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == f"Unregistered {existing_email} from {activity_name}"


class TestRootEndpoint:
    """Test cases for the root endpoint"""
    
    def test_root_redirect(self, client, backup_activities):
        """Test that root endpoint redirects to static index.html"""
        response = client.get("/", follow_redirects=False)
        
        assert response.status_code == 307
        assert response.headers["location"] == "/static/index.html"


class TestIntegrationScenarios:
    """Integration tests covering complete user workflows"""
    
    def test_complete_signup_and_unregister_workflow(self, client, backup_activities):
        """Test a complete workflow: signup -> verify -> unregister -> verify"""
        activity_name = "Art Workshop"
        email = "workflow@mergington.edu"
        
        # Step 1: Sign up for activity
        signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
        assert signup_response.status_code == 200
        
        # Step 2: Verify participant is in the list
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert email in activities_data[activity_name]["participants"]
        
        # Step 3: Unregister from activity
        unregister_response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
        assert unregister_response.status_code == 200
        
        # Step 4: Verify participant is no longer in the list
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert email not in activities_data[activity_name]["participants"]
    
    def test_multiple_participants_same_activity(self, client, backup_activities):
        """Test multiple participants signing up for the same activity"""
        activity_name = "Science Club"
        emails = ["student1@mergington.edu", "student2@mergington.edu", "student3@mergington.edu"]
        
        # Get initial participant count
        initial_response = client.get("/activities")
        initial_data = initial_response.json()
        initial_count = len(initial_data[activity_name]["participants"])
        
        # Sign up all participants
        for email in emails:
            response = client.post(f"/activities/{activity_name}/signup?email={email}")
            assert response.status_code == 200
        
        # Verify all participants are registered
        final_response = client.get("/activities")
        final_data = final_response.json()
        final_participants = final_data[activity_name]["participants"]
        
        assert len(final_participants) == initial_count + len(emails)
        for email in emails:
            assert email in final_participants
    
    def test_participant_capacity_tracking(self, client, backup_activities):
        """Test that participant counts are tracked correctly"""
        # Get initial state
        response = client.get("/activities")
        data = response.json()
        
        # Verify each activity has correct participant count structure
        for activity_name, details in data.items():
            assert "participants" in details
            assert "max_participants" in details
            assert len(details["participants"]) <= details["max_participants"]
            assert isinstance(details["participants"], list)
            assert isinstance(details["max_participants"], int)


class TestErrorHandling:
    """Test cases for error handling and edge cases"""
    
    def test_missing_email_parameter(self, client, backup_activities):
        """Test signup without email parameter"""
        activity_name = "Chess Club"
        
        response = client.post(f"/activities/{activity_name}/signup")
        
        # FastAPI should return 422 for missing required query parameter
        assert response.status_code == 422
    
    def test_empty_email_parameter(self, client, backup_activities):
        """Test signup with empty email parameter"""
        activity_name = "Chess Club"
        
        response = client.post(f"/activities/{activity_name}/signup?email=")
        
        assert response.status_code == 200  # Our API doesn't validate email format
        
        # But verify it was added (even though it's empty)
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert "" in activities_data[activity_name]["participants"]