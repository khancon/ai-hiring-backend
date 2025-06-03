from openai import OpenAI
from app.config import Config
import logging

client = OpenAI(
    api_key=Config.OPENAI_API_KEY
)
logger = logging.getLogger(__name__)

# =========================================
# 1. Job Description Generator
# =========================================
def generate_job_description(title, seniority, skills, location="remote", description=None):
    """
    Uses OpenAI to generate a job description for the given parameters.

    Parameters:
    - title (str): The job title (e.g., "Software Engineer").
    - seniority (str): The seniority level (e.g., "Junior", "Mid-level", "Senior").
    - skills (list): List of required skills (e.g., ["Python", "Flask"]).
    - location (str): Job location (default is "remote").
    - description (str): Optional extra description of the role.
    Returns:
    - str: Generated job description.
    Raises:
    - ValueError: If required parameters are missing or invalid.
    - RuntimeError: If OpenAI API call fails. 
    """
    try:
        if not title or not skills:
            raise ValueError("Title and skills are required to generate a job description.")
        if not location:
            location = "remote"
        if not seniority:
            raise ValueError("Seniority level is required to generate a job description.")
        if not isinstance(skills, list) or not all(isinstance(skill, str) for skill in skills):
            raise ValueError("Skills must be a list of strings.")
        
        prompt = (
            f"Write a detailed job description for a {seniority} {title} role. "
            f"Key skills: {', '.join(skills)}. "
            f"Location: {location}."
            f"{' Extra Description of Role: ' + description if description else ''}"
        )
    
        logger.info(f"Generating job description for {title} ({seniority}) with skills {skills} at {location}")
        response = client.chat.completions.create(
            model=Config.OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}]
        )
    except Exception as e:
        logger.error(f"Error generating job description: {e}")
        raise RuntimeError("Failed to generate job description")
    
    logger.info("Job description generated successfully")
    return response.choices[0].message.content.strip()


# =========================================
# 2. Resume Screening & Fit Scoring
# =========================================
def screen_resume(job_desc, resume_text):
    """
    Uses OpenAI to analyze a candidate resume against a job description.
    Outputs a fit score, strengths, weaknesses, and missing skills.

    Parameters:
    - job_desc (str): The job description to screen against.
    - resume_text (str): The candidate's resume text.
    Returns:
    - str: Analysis result containing fit score, strengths, weaknesses, and missing skills.
    Raises:
    - ValueError: If required parameters are missing or invalid.
    - RuntimeError: If OpenAI API call fails.   
    """
    
    try:
        if not job_desc or not resume_text:
            raise ValueError("Job description and resume text are required for screening.")
        if not isinstance(resume_text, str):
            raise ValueError("Resume text must be a string.")
        if not isinstance(job_desc, str):
            raise ValueError("Job description must be a string.")
        if not resume_text.strip():
            raise ValueError("Resume text cannot be empty.")
        if not job_desc.strip():
            raise ValueError("Job description cannot be empty.")
        
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

        logger.info("Screening resume against job description")
        response = client.chat.completions.create(
            model=Config.OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}]
        )
    except Exception as e:
        logger.error(f"Error screening resume: {e}")
        raise RuntimeError("Failed to screen resume")
    
    logger.info("Resume screening completed successfully")
    return response.choices[0].message.content.strip()


# =========================================
# 3. Screening Questions Generator
# =========================================
def generate_screening_questions(title, skills):
    """
    Uses OpenAI to generate 3-5 screening questions for the specified job title and skills.

    Parameters:
    - title (str): The job title (e.g., "Software Engineer").
    - skills (list): List of required skills (e.g., ["Python", "Flask"]).
    Returns:
    - str: Generated screening questions.
    Raises:
    - ValueError: If required parameters are missing or invalid.
    - RuntimeError: If OpenAI API call fails.
    """
    
    try:
        if not title or not skills:
            raise ValueError("Title and skills are required to generate questions.")
        if not isinstance(skills, list) or not all(isinstance(skill, str) for skill in skills):
            raise ValueError("Skills must be a list of strings.")
        if not skills:
            raise ValueError("Skills list cannot be empty.")
        if len(skills) < 1:
            raise ValueError("At least one skill is required to generate questions.")

        prompt = (
            f"Generate 5 screening questions for a {title} position that requires these skills: {', '.join(skills)}."
        )   
        
        logger.info(f"Generating screening questions for {title} with skills {skills}")
        response = client.chat.completions.create(
            model=Config.OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}]
        )
    except Exception as e:
        logger.error(f"Error generating screening questions: {e}")
        raise RuntimeError("Failed to generate screening questions")
    
    logger.info("Screening questions generated successfully")
    return response.choices[0].message.content.strip()


# =========================================
# 4. Candidate Answer Evaluation
# =========================================
def evaluate_candidate_answers(questions, answers):
    """
    Uses OpenAI to score candidate answers to screening questions and provide feedback.

    Parameters:
    - questions (str): The screening questions.
    - answers (str): The candidate's answers to the questions.
    Returns:
    - str: Evaluation of the candidate's answers, including scores and feedback.
    Raises:
    - ValueError: If required parameters are missing or invalid.
    - RuntimeError: If OpenAI API call fails.
    """
    try:
        if not questions or not answers:
            raise ValueError("Both questions and answers are required for evaluation.")
        if not isinstance(questions, str) or not isinstance(answers, str):
            raise ValueError("Questions and answers must be strings.")
        if not questions.strip():
            raise ValueError("Questions cannot be empty.")
        if not answers.strip():
            raise ValueError("Answers cannot be empty.")

        prompt = (
            "You are an AI interviewer. Here are some screening questions and a candidate's answers.\n\n"
            f"Questions:\n{questions}\n\n"
            f"Answers:\n{answers}\n\n"
            "Score each answer from 1–10 and explain your evaluation."
        )

        logger.info("Evaluating candidate answers")
        response = client.chat.completions.create(
            model=Config.OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}]
        )
    except Exception as e:
        logger.error(f"Error evaluating candidate answers: {e}")
        raise RuntimeError("Failed to evaluate candidate answers")
    
    logger.info("Candidate answers evaluated successfully")
    return response.choices[0].message.content.strip()


# =========================================
# 5. Feedback Email Generator
# =========================================
def generate_feedback_email(candidate_name, job_title, outcome, tone="professional"):
    """
    Uses OpenAI to generate a personalized feedback email (acceptance or rejection).

    Parameters:
    - candidate_name (str): The name of the candidate.
    - job_title (str): The job title for which the candidate applied.
    - outcome (str): The outcome of the application ('accepted' or 'rejected').
    - tone (str): The tone of the email ('professional', 'friendly', 'formal').
    Returns:
    - str: Generated feedback email content.
    Raises:
    - ValueError: If required parameters are missing or invalid.
    - RuntimeError: If OpenAI API call fails.
    """
    try:
        if not candidate_name or not job_title or not outcome:
            raise ValueError("Candidate name, job title, and outcome are required.")
        if outcome not in ['accepted', 'rejected']:
            raise ValueError("Outcome must be either 'accepted' or 'rejected'.")
        if tone not in ['professional', 'friendly', 'formal']:
            raise ValueError("Tone must be one of: professional, friendly, formal.")
        
        candidate_name = candidate_name.strip()
        job_title = job_title.strip()

        if outcome == 'accepted':
            status_text = 'acceptance'
        else:
            status_text = 'rejection'

        prompt = (
            f"Write a {tone} {status_text} email to {candidate_name} for the position of {job_title}. "
            "Include one sentence of general positive feedback."
        )

        logger.info(f"Generating feedback email for {candidate_name} ({job_title}) with outcome {outcome} and tone {tone}")
        response = client.chat.completions.create(
            model=Config.OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}]
        )
    except Exception as e:
        logger.error(f"Error generating feedback email: {e}")
        raise RuntimeError("Failed to generate feedback email")
    
    logger.info("Feedback email generated successfully")
    return response.choices[0].message.content.strip()
