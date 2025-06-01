from flask import Blueprint, request, jsonify
from app.services import openai_service
from app.utils.resume_parser import extract_text_from_resume

# Create the Blueprint for AI-related routes
ai_bp = Blueprint("ai", __name__)

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
    jd = openai_service.generate_job_description(title, seniority, skills, location)
    return jsonify({"job_description": jd})

# -----------------------------------------
# 2. Resume Screening & Fit Scoring
# -----------------------------------------
@ai_bp.route("/screen-resume", methods=["POST"])
def screen_resume():
    # Expect multipart/form-data with a resume file and job description as text
    job_desc = request.form.get("job_description")
    resume_file = request.files.get("resume")
    if not (job_desc and resume_file):
        return jsonify({"error": "Missing required fields"}), 400

    # Extract resume text
    resume_text = extract_text_from_resume(resume_file)
    # Call the service function
    result = openai_service.screen_resume(job_desc, resume_text)
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
    questions = openai_service.generate_screening_questions(title, skills)
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
    evaluation = openai_service.evaluate_candidate_answers(questions, answers)
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
    email = openai_service.generate_feedback_email(candidate_name, job_title, outcome, tone)
    return jsonify({"email": email})
