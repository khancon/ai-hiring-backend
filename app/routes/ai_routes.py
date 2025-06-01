from flask import Blueprint, request, jsonify
from app.services import openai_service
from app.utils.resume_parser import extract_text_from_resume
import logging

# Create the Blueprint for AI-related routes
ai_bp = Blueprint("ai", __name__)
logger = logging.getLogger(__name__)
# -----------------------------------------
# 1. Job Description Generator
# -----------------------------------------
@ai_bp.route("/generate-jd", methods=["POST"])
def generate_jd():
    # Get the job details from the JSON request body
    data = request.json
    title = data.get("title")
    seniority = data.get("seniority", "")
    skills = data.get("skills", [])
    location = data.get("location", "remote")

    # Call the service function
    try:
        if not title or not skills:
            logger.error("Title or skills missing in request")
            return jsonify({"error": "Title and skills are required"}), 400
        
        logger.info(f"Generating job description for {title} ({seniority}) with skills {skills} at {location}")
        jd = openai_service.generate_job_description(title, seniority, skills, location)
    except Exception as e:
        logger.error(f"Error generating job description: {e}")
        return jsonify({"error": "Failed to generate job description"}), 500
    
    logger.info("Job description generated successfully")
    return jsonify({"job_description": jd})

# -----------------------------------------
# 2. Resume Screening & Fit Scoring
# -----------------------------------------
@ai_bp.route("/screen-resume", methods=["POST"])
def screen_resume():
    # Expect multipart/form-data with a resume file and job description as text
    job_desc = request.form.get("job_description")
    resume_file = request.files.get("resume")

    # Extract resume text
    try:
        if not (job_desc and resume_file):
            logger.error("Missing job description or resume file")
            return jsonify({"error": "Missing required fields"}), 400
        
        logger.info("Extracting text from resume file")
        resume_text = extract_text_from_resume(resume_file)
    except Exception as e:
        logger.error(f"Error extracting text from resume: {e}")
        return jsonify({"error": "Failed to extract resume text"}), 500
    
    # Call the service function
    try:
        if not resume_text.strip():
            logger.warning("Resume text is empty after extraction")
            return jsonify({"error": "Resume text is empty"}), 400
        if not job_desc.strip():
            logger.warning("Job description is empty")
            return jsonify({"error": "Job description is empty"}), 400
        
        logger.info(f"Screening resume for job description: {job_desc[:50]}...")  # Log first 50 chars
        result = openai_service.screen_resume(job_desc, resume_text)
    except Exception as e:
        logger.error(f"Error screening resume: {e}")
        return jsonify({"error": "Failed to screen resume"}), 500
    
    logger.info("Resume screening completed successfully")
    return jsonify({"screening_result": result})

# -----------------------------------------
# 3. Screening Questions Generator
# -----------------------------------------
@ai_bp.route("/generate-questions", methods=["POST"])
def generate_questions():
    # Get job title and skills from request JSON
    data = request.json
    title = data.get("title")
    skills = data.get("skills", [])

    # Call the service function
    try:
        if not title or not skills:
            logger.error("Title or skills missing in request")
            return jsonify({"error": "Title and skills are required"}), 400
        logger.info(f"Generating screening questions for {title} with skills {skills}")
        if not isinstance(skills, list) or not all(isinstance(skill, str) for skill in skills):
            logger.error("Skills must be a list of strings")
            return jsonify({"error": "Skills must be a list of strings"}), 400
        if len(skills) < 1:
            logger.error("At least one skill is required")
            return jsonify({"error": "At least one skill is required"}), 400
        
        logger.info(f"Generating questions for title: {title}, skills: {skills}")
        questions = openai_service.generate_screening_questions(title, skills)
    except Exception as e:
        logger.error(f"Error generating screening questions: {e}")
        return jsonify({"error": "Failed to generate screening questions"}), 500
    
    logger.info("Screening questions generated successfully")
    return jsonify({"questions": questions})

# -----------------------------------------
# 4. Candidate Answer Evaluation
# -----------------------------------------
@ai_bp.route("/evaluate", methods=["POST"])
def evaluate_candidate_answers():
    # Get questions and answers from request JSON
    data = request.json
    questions = data.get("questions")
    answers = data.get("answers")

    # Call the service function
    try:
        if not questions or not answers:
            logger.error("Questions or answers missing in request")
            return jsonify({"error": "Questions and answers are required"}), 400
        
        logger.info("Evaluating candidate answers")
        evaluation = openai_service.evaluate_candidate_answers(questions, answers)
    except Exception as e:
        logger.error(f"Error evaluating candidate answers: {e}")
        return jsonify({"error": "Failed to evaluate candidate answers"}), 500
    
    logger.info("Candidate answers evaluated successfully")
    return jsonify({"evaluation": evaluation})

# -----------------------------------------
# 5. Feedback Email Generator
# -----------------------------------------
@ai_bp.route("/generate-feedback", methods=["POST"])
def generate_feedback_email():
    # Get candidate info and outcome from request JSON
    data = request.json
    candidate_name = data.get("candidate_name")
    job_title = data.get("job_title")
    outcome = data.get("outcome")
    tone = data.get("tone", "professional")

    # Call the service function
    try:
        if not candidate_name or not job_title or not outcome:
            logger.error("Candidate name, job title, and outcome are required")
            return jsonify({"error": "Candidate name, job title, and outcome are required"}), 400
        
        logger.info(f"Generating feedback email for {candidate_name} for {job_title} with outcome {outcome}")
        if outcome not in ["accepted", "rejected"]:
            logger.error("Outcome must be 'accepted' or 'rejected'")
            return jsonify({"error": "Outcome must be 'accepted' or 'rejected'"}), 400
        if tone not in ["professional", "friendly", "formal"]:
            logger.error("Tone must be 'professional', 'friendly', or 'formal'")
            return jsonify({"error": "Tone must be 'professional', 'friendly', or 'formal'"}), 400
        
        logger.info(f"Generating feedback email with tone: {tone}")         
        email = openai_service.generate_feedback_email(candidate_name, job_title, outcome, tone)
    except Exception as e:
        logger.error(f"Error generating feedback email: {e}")
        return jsonify({"error": "Failed to generate feedback email"}), 500
    
    logger.info("Feedback email generated successfully")
    return jsonify({"email": email})
