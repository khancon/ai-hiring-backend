import io
import pytest
from unittest.mock import patch, MagicMock

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

def test_generate_jd_with_description(client):
    description = "This role will focus on building APIs and mentoring junior engineers."
    # We want to check that the service is called with the correct args, including description
    with patch("app.services.openai_service.generate_job_description", return_value="JD with Description") as mock_generate_jd:
        response = client.post("/generate-jd", json={
            "title": "Backend Engineer",
            "seniority": "Senior",
            "skills": ["Python", "Flask"],
            "location": "Remote",
            "description": description
        })
        assert response.status_code == 200
        data = response.get_json()
        assert "job_description" in data
        assert data["job_description"] == "JD with Description"
        # Check description is actually passed to the service function
        mock_generate_jd.assert_called_once_with(
            "Backend Engineer", "Senior", ["Python", "Flask"], "Remote", description
        )

def test_generate_jd_empty_location(client):
    with patch("app.services.openai_service.generate_job_description", return_value="JD for remote") as mock_generate_jd:
        response = client.post("/generate-jd", json={
            "title": "Backend Engineer",
            "skills": ["Python", "Flask"],
            "seniority": "Senior"
            # "location": ""  # Empty string triggers default
        })
        assert response.status_code == 200
        data = response.get_json()
        assert data["job_description"] == "JD for remote"
        mock_generate_jd.assert_called_once_with(
            "Backend Engineer", "Senior", ["Python", "Flask"], "remote", None
        )

def test_generate_jd_missing_seniority(client):
    with patch("app.services.openai_service.generate_job_description", side_effect=ValueError("Seniority level is required to generate a job description.")), \
         patch("app.routes.ai_routes.logger") as mock_logger:
        response = client.post("/generate-jd", json={
            "title": "Backend Engineer",
            "skills": ["Python", "Flask"],
            # "seniority" is omitted
            "location": "Remote"
        })
        assert response.status_code == 500
        data = response.get_json()
        assert "Failed to generate job description" in data["error"]
        # Confirm logger.error was called
        error_calls = [call for call in mock_logger.error.call_args_list if "Seniority level is required" in str(call)]
        assert len(error_calls) >= 1

def test_generate_jd_skills_not_list(client):
    with patch("app.services.openai_service.generate_job_description", side_effect=ValueError("Skills must be a list of strings.")), \
         patch("app.routes.ai_routes.logger") as mock_logger:
        response = client.post("/generate-jd", json={
            "title": "Backend Engineer",
            "skills": "Python, Flask",  # Not a list!
            "seniority": "Senior",
            "location": "Remote"
        })
        assert response.status_code == 500
        data = response.get_json()
        assert "Failed to generate job description" in data["error"]
        # Confirm logger.error was called
        error_calls = [call for call in mock_logger.error.call_args_list if "Skills must be a list of strings." in str(call)]
        assert len(error_calls) >= 1

def test_generate_jd_skills_contains_non_str(client):
    with patch("app.services.openai_service.generate_job_description", side_effect=ValueError("Skills must be a list of strings.")), \
         patch("app.routes.ai_routes.logger") as mock_logger:
        response = client.post("/generate-jd", json={
            "title": "Backend Engineer",
            "skills": ["Python", 42],  # 42 is not a str
            "seniority": "Senior",
            "location": "Remote"
        })
        assert response.status_code == 500
        data = response.get_json()
        assert "Failed to generate job description" in data["error"]
        error_calls = [call for call in mock_logger.error.call_args_list if "Skills must be a list of strings." in str(call)]
        assert len(error_calls) >= 1

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

def test_screen_resume_extract_text_failure(client):
    # Use MagicMock to simulate file upload
    dummy_file = MagicMock()
    data = {
        "job_description": "Some JD"
    }
    # Patch extract_text_from_resume to raise Exception
    with patch("app.routes.ai_routes.extract_text_from_resume", side_effect=Exception("PDF extraction failed")), \
         patch("app.routes.ai_routes.logger") as mock_logger:
        response = client.post(
            "/screen-resume",
            data={
                "job_description": data["job_description"],
                "resume": (dummy_file, "resume.pdf")
            },
            content_type="multipart/form-data"
        )
        assert response.status_code == 500
        result = response.get_json()
        assert result["error"] == "Failed to extract resume text"
        # Confirm logger was called
        assert any("Error extracting text from resume" in str(call) for call in mock_logger.error.call_args_list)

def test_screen_resume_empty_resume_text(client):
    dummy_file = MagicMock()
    with patch("app.routes.ai_routes.extract_text_from_resume", return_value=""), \
         patch("app.routes.ai_routes.logger") as mock_logger:
        response = client.post(
            "/screen-resume",
            data={
                "job_description": "Some JD",
                "resume": (dummy_file, "resume.pdf")
            },
            content_type="multipart/form-data"
        )
        assert response.status_code == 400
        result = response.get_json()
        assert result["error"] == "Resume text is empty"
        # Confirm warning was logged
        assert any("Resume text is empty after extraction" in str(call) for call in mock_logger.warning.call_args_list)

def test_screen_resume_screening_service_exception(client):
    dummy_file = MagicMock()
    with patch("app.routes.ai_routes.extract_text_from_resume", return_value="Some resume text"), \
         patch("app.routes.ai_routes.openai_service.screen_resume", side_effect=Exception("Service fail")), \
         patch("app.routes.ai_routes.logger") as mock_logger:
        response = client.post(
            "/screen-resume",
            data={
                "job_description": "Valid JD",
                "resume": (dummy_file, "resume.pdf")
            },
            content_type="multipart/form-data"
        )
        assert response.status_code == 500
        result = response.get_json()
        assert result["error"] == "Failed to screen resume"
        assert any("Error screening resume" in str(call) for call in mock_logger.error.call_args_list)

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

def test_generate_questions_missing_title(client):
    # Patch service to ensure no external call
    with patch("app.routes.ai_routes.openai_service.generate_screening_questions"):
        response = client.post("/generate-questions", json={
            "skills": ["Python", "Flask"]
        })
        assert response.status_code == 400
        data = response.get_json()
        assert data["error"] == "Title and skills are required"

def test_generate_questions_missing_skills(client):
    with patch("app.routes.ai_routes.openai_service.generate_screening_questions"):
        response = client.post("/generate-questions", json={
            "title": "Backend Engineer"
        })
        assert response.status_code == 400
        data = response.get_json()
        assert data["error"] == "Title and skills are required"

def test_generate_questions_skills_not_list(client):
    with patch("app.routes.ai_routes.openai_service.generate_screening_questions"):
        response = client.post("/generate-questions", json={
            "title": "Backend Engineer",
            "skills": "Python,Flask"
        })
        assert response.status_code == 400
        data = response.get_json()
        assert data["error"] == "Skills must be a list of strings"

def test_generate_questions_skills_contains_non_string(client):
    with patch("app.routes.ai_routes.openai_service.generate_screening_questions"):
        response = client.post("/generate-questions", json={
            "title": "Backend Engineer",
            "skills": ["Python", 123]
        })
        assert response.status_code == 400
        data = response.get_json()
        assert data["error"] == "Skills must be a list of strings"

def test_generate_questions_skills_empty(client):
    with patch("app.routes.ai_routes.openai_service.generate_screening_questions"):
        response = client.post("/generate-questions", json={
            "title": "Backend Engineer",
            "skills": []
        })
        assert response.status_code == 400
        data = response.get_json()
        assert data["error"] == "Title and skills are required"

def test_generate_questions_openai_exception(client):
    with patch("app.routes.ai_routes.openai_service.generate_screening_questions", side_effect=Exception("OpenAI error")), \
         patch("app.routes.ai_routes.logger") as mock_logger:
        response = client.post("/generate-questions", json={
            "title": "Backend Engineer",
            "skills": ["Python", "Flask"]
        })
        assert response.status_code == 500
        data = response.get_json()
        assert data["error"] == "Failed to generate screening questions"
        error_calls = [call for call in mock_logger.error.call_args_list if "Error generating screening questions" in str(call)]
        assert len(error_calls) >= 1  # Confirm error was logged


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
