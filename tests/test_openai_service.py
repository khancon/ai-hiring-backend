from unittest.mock import patch
from app.services import openai_service

def fake_openai_response(content):
    # Helper to mimic OpenAI's response object
    FakeMsg = type("FakeMsg", (object,), {"content": content})
    FakeChoice = type("FakeChoice", (object,), {"message": FakeMsg()})
    return type("FakeResp", (object,), {"choices": [FakeChoice()]})()

def test_generate_job_description():
    # Test for the Job Description Generator function
    title = "Backend Engineer"
    seniority = "Senior"
    skills = ["Python", "Flask", "SQL"]
    location = "Remote"
    with patch("openai.ChatCompletion.create", return_value=fake_openai_response("Backend Engineer JD here")):
        jd = openai_service.generate_job_description(title, seniority, skills, location)
    assert isinstance(jd, str)
    assert len(jd.strip()) > 0, "Job description should not be empty."
    assert "Backend Engineer" in jd or "backend engineer" in jd.lower()

def test_screen_resume():
    # Test for the Resume Screening & Fit Scoring function
    job_desc = "We are looking for a Python developer with experience in Flask and SQL."
    resume_text = (
        "John Doe\n"
        "Experienced Python developer. Worked on Flask web apps for 3 years. Strong knowledge of SQL."
    )
    mock_content = "Fit score: 90\nStrengths: ...\nAreas for improvement: ..."
    with patch("openai.ChatCompletion.create", return_value=fake_openai_response(mock_content)):
        result = openai_service.screen_resume(job_desc, resume_text)
    assert isinstance(result, str)
    assert len(result.strip()) > 0, "Screening result should not be empty."
    assert "Fit score" in result or "fit score" in result.lower()
    assert "strength" in result.lower()
    assert "improvement" in result.lower()

def test_generate_screening_questions():
    # Test for the Screening Questions Generator function
    title = "Frontend Engineer"
    skills = ["React", "JavaScript", "CSS"]
    mock_questions = "1. What is React?\n2. How do you use CSS?\n3. Explain JavaScript closures."
    with patch("openai.ChatCompletion.create", return_value=fake_openai_response(mock_questions)):
        questions = openai_service.generate_screening_questions(title, skills)
    assert isinstance(questions, str)
    assert len(questions.strip()) > 0, "Generated questions should not be empty."
    question_lines = [line for line in questions.split("\n") if line.strip()]
    assert len(question_lines) >= 3, "Should generate at least 3 questions."
    assert any("?" in q or "question" in q.lower() for q in question_lines)

def test_evaluate_candidate_answers():
    # Test for the Candidate Answer Evaluation function
    questions = (
        "1. What is your experience with React?\n"
        "2. How do you manage component state?"
    )
    answers = (
        "1. I have 2 years of experience building apps in React.\n"
        "2. I use React hooks like useState and useReducer."
    )
    mock_eval = "Score: 9/10 for both answers.\nFeedback: Great experience!"
    with patch("openai.ChatCompletion.create", return_value=fake_openai_response(mock_eval)):
        evaluation = openai_service.evaluate_candidate_answers(questions, answers)
    assert isinstance(evaluation, str)
    assert len(evaluation.strip()) > 0, "Evaluation output should not be empty."
    assert "score" in evaluation.lower() or "evaluation" in evaluation.lower() or "feedback" in evaluation.lower()

def test_generate_feedback_email():
    # Test for the Feedback Email Generator function
    candidate_name = "Jane Smith"
    job_title = "Data Scientist"
    outcome = "rejected"
    tone = "friendly"
    mock_email = "Dear Jane, thank you for applying to Data Scientist. We wish you luck!"
    with patch("openai.ChatCompletion.create", return_value=fake_openai_response(mock_email)):
        email = openai_service.generate_feedback_email(candidate_name, job_title, outcome, tone)
    assert isinstance(email, str)
    assert len(email.strip()) > 0, "Feedback email should not be empty."
    assert (
        "Jane Smith" in email
        or "jane smith" in email.lower()
        or "Jane" in email
        or "jane" in email.lower()
    ), "Candidate's name (first or full) should appear in the email."
    assert "Data Scientist" in email or "data scientist" in email.lower()

def test_generate_job_description_empty_skills():
    # Should handle empty skills gracefully
    title = "DevOps Engineer"
    seniority = "Mid"
    skills = []
    location = "Onsite"
    with patch("openai.ChatCompletion.create", return_value=fake_openai_response("DevOps JD")):
        jd = openai_service.generate_job_description(title, seniority, skills, location)
    assert isinstance(jd, str)
    assert "DevOps" in jd or "devops" in jd.lower()

def test_screen_resume_missing_keywords():
    # Should mention missing skills if resume lacks them
    job_desc = "Looking for a Go developer with Kubernetes experience."
    resume_text = "Jane Doe\nExperienced in Python and Docker."
    mock_content = "Fit score: 40\nStrengths: ...\nAreas for improvement: ...\nMissing skills: Go, Kubernetes"
    with patch("openai.ChatCompletion.create", return_value=fake_openai_response(mock_content)):
        result = openai_service.screen_resume(job_desc, resume_text)
    assert "Missing skills" in result or "missing skills" in result.lower()
    assert "Go" in result or "Kubernetes" in result

def test_generate_feedback_email_acceptance():
    # Should generate an acceptance email
    candidate_name = "Alex Johnson"
    job_title = "ML Engineer"
    outcome = "accepted"
    tone = "enthusiastic"
    mock_email = "Congratulations Alex, you have been accepted for the ML Engineer role!"
    with patch("openai.ChatCompletion.create", return_value=fake_openai_response(mock_email)):
        email = openai_service.generate_feedback_email(candidate_name, job_title, outcome, tone)
    assert "accepted" in email.lower() or "congratulations" in email.lower()
    assert "Alex" in email or "alex" in email.lower()
    assert "ML Engineer" in email or "ml engineer" in email.lower()