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
