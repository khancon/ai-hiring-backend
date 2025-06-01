from openai import OpenAI
from app.config import Config

client = OpenAI(
    api_key=Config.OPENAI_API_KEY
)

# =========================================
# 1. Job Description Generator
# =========================================
def generate_job_description(title, seniority, skills, location="remote"):
    """
    Uses OpenAI to generate a job description for the given parameters.
    """
    prompt = (
        f"Write a detailed job description for a {seniority} {title} role. "
        f"Key skills: {', '.join(skills)}. "
        f"Location: {location}."
    )
    response = client.chat.completions.create(
        model=Config.OPENAI_MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()


# =========================================
# 2. Resume Screening & Fit Scoring
# =========================================
def screen_resume(job_desc, resume_text):
    """
    Uses OpenAI to analyze a candidate resume against a job description.
    Outputs a fit score, strengths, weaknesses, and missing skills.
    """
    prompt = (
        "You are an AI hiring assistant. Evaluate the following resume for the job below.\n\n"
        f"Job Description:\n{job_desc}\n\n"
        f"Resume:\n{resume_text}\n\n"
        "Provide:\n"
        "- Fit score out of 100\n"
        "- 3 strengths\n"
        "- 3 areas for improvement\n"
        "- Any missing keywords or skills"
    )
    response = client.chat.completions.create(
        model=Config.OPENAI_MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()


# =========================================
# 3. Screening Questions Generator
# =========================================
def generate_screening_questions(title, skills):
    """
    Uses OpenAI to generate 3-5 screening questions for the specified job title and skills.
    """
    prompt = (
        f"Generate 5 screening questions for a {title} position that requires these skills: {', '.join(skills)}."
    )
    response = client.chat.completions.create(
        model=Config.OPENAI_MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()


# =========================================
# 4. Candidate Answer Evaluation
# =========================================
def evaluate_candidate_answers(questions, answers):
    """
    Uses OpenAI to score candidate answers to screening questions and provide feedback.
    """
    prompt = (
        "You are an AI interviewer. Here are some screening questions and a candidate's answers.\n\n"
        f"Questions:\n{questions}\n\n"
        f"Answers:\n{answers}\n\n"
        "Score each answer from 1–10 and explain your evaluation."
    )
    response = client.chat.completions.create(
        model=Config.OPENAI_MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()


# =========================================
# 5. Feedback Email Generator
# =========================================
def generate_feedback_email(candidate_name, job_title, outcome, tone="professional"):
    """
    Uses OpenAI to generate a personalized feedback email (acceptance or rejection).
    """
    if outcome == 'accepted':
        status_text = 'acceptance'
    else:
        status_text = 'rejection'
    prompt = (
        f"Write a {tone} {status_text} email to {candidate_name} for the position of {job_title}. "
        "Include one sentence of general positive feedback."
    )
    response = client.chat.completions.create(
        model=Config.OPENAI_MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()
