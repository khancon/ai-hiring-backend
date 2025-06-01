from app.services import openai_service

def test_generate_job_description():
    # Test for the Job Description Generator function
    
    # Define sample input parameters
    title = "Backend Engineer"
    seniority = "Senior"
    skills = ["Python", "Flask", "SQL"]
    location = "Remote"
    
    # Call the function with sample inputs
    jd = openai_service.generate_job_description(title, seniority, skills, location)
    
    # Check that the output is a non-empty string
    assert isinstance(jd, str)
    assert len(jd.strip()) > 0, "Job description should not be empty."
    
    # Check that the job title appears in the generated description
    assert "Backend Engineer" in jd or "backend engineer" in jd.lower()
    

def test_screen_resume():
    # Test for the Resume Screening & Fit Scoring function
    
    # Provide a sample job description and a sample resume text
    job_desc = "We are looking for a Python developer with experience in Flask and SQL."
    resume_text = (
        "John Doe\n"
        "Experienced Python developer. Worked on Flask web apps for 3 years. Strong knowledge of SQL."
    )
    
    # Call the function with sample data
    result = openai_service.screen_resume(job_desc, resume_text)
    
    # Check that the output is a non-empty string
    assert isinstance(result, str)
    assert len(result.strip()) > 0, "Screening result should not be empty."
    
    # Look for expected keywords in the result
    assert "Fit score" in result or "fit score" in result.lower()
    assert "strength" in result.lower()
    assert "improvement" in result.lower()
    

def test_generate_screening_questions():
    # Test for the Screening Questions Generator function
    
    # Provide a sample job title and skills list
    title = "Frontend Engineer"
    skills = ["React", "JavaScript", "CSS"]
    
    # Call the function to generate questions
    questions = openai_service.generate_screening_questions(title, skills)
    
    # Check that the output is a non-empty string
    assert isinstance(questions, str)
    assert len(questions.strip()) > 0, "Generated questions should not be empty."
    
    # Check that there are at least 3 questions (assuming each is on a new line or numbered)
    question_lines = [line for line in questions.split("\n") if line.strip()]
    assert len(question_lines) >= 3, "Should generate at least 3 questions."
    assert any("?" in q or "question" in q.lower() for q in question_lines)
    

def test_evaluate_candidate_answers():
    # Test for the Candidate Answer Evaluation function
    
    # Provide sample screening questions and candidate answers
    questions = (
        "1. What is your experience with React?\n"
        "2. How do you manage component state?"
    )
    answers = (
        "1. I have 2 years of experience building apps in React.\n"
        "2. I use React hooks like useState and useReducer."
    )
    
    # Call the evaluation function
    evaluation = openai_service.evaluate_candidate_answers(questions, answers)
    
    # Check that the output is a non-empty string
    assert isinstance(evaluation, str)
    assert len(evaluation.strip()) > 0, "Evaluation output should not be empty."
    
    # Check that scores and feedback keywords appear in the output
    assert "score" in evaluation.lower() or "evaluation" in evaluation.lower() or "feedback" in evaluation.lower()
    

def test_generate_feedback_email():
    # Test for the Feedback Email Generator function
    
    # Provide sample candidate info and job details
    candidate_name = "Jane Smith"
    job_title = "Data Scientist"
    outcome = "rejected"
    tone = "friendly"
    
    # Generate feedback email
    email = openai_service.generate_feedback_email(candidate_name, job_title, outcome, tone)
    
    # Check that the output is a non-empty string
    assert isinstance(email, str)
    assert len(email.strip()) > 0, "Feedback email should not be empty."
    
    # Check for presence of candidate name and job title in email
    # Check for presence of candidate name (first or full) and job title in email
    assert (
        "Jane Smith" in email
        or "jane smith" in email.lower()
        or "Jane" in email
        or "jane" in email.lower()
    ), "Candidate's name (first or full) should appear in the email."
    assert "Data Scientist" in email or "data scientist" in email.lower()


# You can run these with pytest or just python -m pytest tests/
