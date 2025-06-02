import io
import pytest
from unittest.mock import patch

from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# -----------------------------------------------
# 1. Test Job Description Generator Route
# -----------------------------------------------
def test_generate_jd_route(client):
    with patch("app.services.openai_service.generate_job_description", return_value="Generated JD"):
        response = client.post("/generate-jd", json={
            "title": "Backend Engineer",
            "seniority": "Senior",
            "skills": ["Python", "Flask"],
            "location": "Remote"
        })
        assert response.status_code == 200
        data = response.get_json()
        assert "job_description" in data
        assert data["job_description"] == "Generated JD"

def test_generate_jd_missing_title(client):
    # Only provide skills, omit title
    response = client.post("/generate-jd", json={
        "skills": ["Python", "Flask"],
        "seniority": "Senior",
        "location": "Remote"
    })
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert "Title and skills are required" in data["error"]

def test_generate_jd_missing_skills(client):
    # Only provide title, omit skills
    response = client.post("/generate-jd", json={
        "title": "Backend Engineer",
        "seniority": "Senior",
        "location": "Remote"
    })
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert "Title and skills are required" in data["error"]

from unittest.mock import patch

def test_generate_jd_openai_exception(client):
    # Patch both the OpenAI call to raise and the logger to spy on error calls
    with patch("app.services.openai_service.generate_job_description", side_effect=Exception("OpenAI error!")), \
         patch("app.routes.ai_routes.logger") as mock_logger:
        
        response = client.post("/generate-jd", json={
            "title": "Backend Engineer",
            "skills": ["Python", "Flask"],
            "seniority": "Senior",
            "location": "Remote"
        })
    
    # Check HTTP error response
    assert response.status_code == 500
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Failed to generate job description"
    
    # Check logger.error was called with appropriate message
    error_calls = [call for call in mock_logger.error.call_args_list if "Error generating job description" in str(call)]
    assert len(error_calls) >= 1  # Should log at least one error


# -----------------------------------------------
# 2. Test Resume Screening & Fit Scoring Route
# -----------------------------------------------
def test_screen_resume_route(client):
    # Patch the function as used in the route module
    with patch("app.routes.ai_routes.extract_text_from_resume", return_value="Resume text here"):
        with patch("app.services.openai_service.screen_resume", return_value="Screened!"):
            data = {
                "job_description": "Python Developer needed."
            }
            fake_pdf = (io.BytesIO(b"%PDF-1.4 mock pdf bytes"), "resume.pdf")
            response = client.post(
                "/screen-resume",
                data={
                    "job_description": data["job_description"],
                    "resume": fake_pdf
                },
                content_type='multipart/form-data'
            )
            assert response.status_code == 200
            result = response.get_json()
            assert "screening_result" in result
            assert result["screening_result"] == "Screened!"

def test_screen_resume_route_missing_fields(client):
    response = client.post("/screen-resume", data={}, content_type='multipart/form-data')
    assert response.status_code == 400
    assert "error" in response.get_json()

# -----------------------------------------------
# 3. Test Screening Questions Generator Route
# -----------------------------------------------
def test_generate_questions_route(client):
    with patch("app.services.openai_service.generate_screening_questions", return_value="Questions..."):
        response = client.post("/generate-questions", json={
            "title": "Frontend Engineer",
            "skills": ["React", "CSS"]
        })
        assert response.status_code == 200
        data = response.get_json()
        assert "questions" in data
        assert data["questions"] == "Questions..."

# -----------------------------------------------
# 4. Test Candidate Answer Evaluation Route
# -----------------------------------------------
def test_evaluate_candidate_answers_route(client):
    with patch("app.services.openai_service.evaluate_candidate_answers", return_value="Eval result!"):
        response = client.post("/evaluate", json={
            "questions": "What is React?",
            "answers": "A JS library."
        })
        assert response.status_code == 200
        data = response.get_json()
        assert "evaluation" in data
        assert data["evaluation"] == "Eval result!"

# -----------------------------------------------
# 5. Test Feedback Email Generator Route
# -----------------------------------------------
def test_generate_feedback_email_route(client):
    with patch("app.services.openai_service.generate_feedback_email", return_value="Feedback email here!"):
        response = client.post("/generate-feedback", json={
            "candidate_name": "Jane Smith",
            "job_title": "Data Scientist",
            "outcome": "rejected",
            "tone": "friendly"
        })
        assert response.status_code == 200
        data = response.get_json()
        assert "email" in data
        assert data["email"] == "Feedback email here!"
