ifneq (,$(wildcard .env))
    include .env
    export
endif

# GIT commands
prune-branches:
	git fetch --prune
	git branch -vv | grep ': gone]' | awk '{print $$1}' | xargs -r git branch -d

# Python virtual environment and package management
.PHONY: install clean update-pip pytest 

install:
	python -m venv venv
	source venv/bin/activate
	pip install -r requirements.txt

clean:
	rm -rf venv
	rm -f requirements.txt

update-pip:
	pip freeze > requirements.txt

pip-compile:
	pip-compile requirements.in
	pip install -r requirements.txt

pytest:
	PYTHONPATH=. pytest --cov=app --cov-report=term-missing tests/
	coverage html

# Test Suites
.PHONY: pytest-ai-routes pytest-openai-service pytest-resume-parser

pytest-ai-routes:
	PYTHONPATH=. pytest tests/test_ai_routes.py

pytest-openai-service:
	PYTHONPATH=. pytest tests/test_openai_service.py

pytest-resume-parser:
	PYTHONPATH=. pytest tests/test_resume_parser.py

# Environment Variables
.PHONY: print-env-vars

print-env-vars:
	@echo "OPEN_API_KEY=${OPEN_API_KEY}"

# Docker commands
.PHONY: docker-build docker-run docker

docker-build:
	docker build -t ai-hiring-backend .

docker-run:
	docker run --env-file .env -p 5000:5000 ai-hiring-backend

docker: docker-build docker-run

# Flask commands
.PHONY: flask-run

flask-run:
	export FLASK_APP=app.py
	export FLASK_ENV=development
	@echo "Running Flask app..."
	flask run

# API Usage Shortcuts
.PHONY: curl-generate-jd curl-screen-resume curl-generate-questions curl-evaluate curl-generate-feedback

curl-generate-jd:
	curl -X POST http://127.0.0.1:5000/generate-jd \
		-H "Content-Type: application/json" \
		-d '{"title":"Backend Engineer", "seniority":"Senior", "skills":["Python","Flask"], "location":"Remote"}' | jq

curl-screen-resume:
	curl -X POST http://127.0.0.1:5000/screen-resume \
		-F "job_description=Looking for a Python developer with Flask experience." \
		-F "resume=@resume.pdf" | jq

curl-generate-questions:
	curl -X POST http://127.0.0.1:5000/generate-questions \
		-H "Content-Type: application/json" \
		-d '{"title":"Frontend Engineer", "skills":["React","CSS"]}' | jq

curl-evaluate:
	curl -X POST http://127.0.0.1:5000/evaluate \
		-H "Content-Type: application/json" \
		-d '{"questions":"1. What is React?\n2. How do you use CSS?", "answers":"1. I have 3 years experience.\n2. I use Flexbox and Grid."}' | jq

curl-generate-feedback:
	curl -X POST http://127.0.0.1:5000/generate-feedback \
		-H "Content-Type: application/json" \
		-d '{"candidate_name":"Jane Doe", "job_title":"Designer", "outcome":"rejected", "tone":"friendly"}' | jq

# Render-hosted API test commands
.PHONY: curl-remote-generate-jd curl-remote-screen-resume curl-remote-generate-questions curl-remote-evaluate curl-remote-generate-feedback

REMOTE_HOST = https://ai-hiring-backend.onrender.com

curl-remote-generate-jd:
	curl -X POST $(REMOTE_HOST)/generate-jd \
		-H "Content-Type: application/json" \
		-d '{"title":"Backend Engineer", "seniority":"Senior", "skills":["Python","Flask"], "location":"Remote"}' | jq

curl-remote-screen-resume:
	curl -X POST $(REMOTE_HOST)/screen-resume \
		-F "job_description=Looking for a Python developer with Flask experience." \
		-F "resume=@resume.pdf" | jq

curl-remote-generate-questions:
	curl -X POST $(REMOTE_HOST)/generate-questions \
		-H "Content-Type: application/json" \
		-d '{"title":"Frontend Engineer", "skills":["React","CSS"]}' | jq

curl-remote-evaluate:
	curl -X POST $(REMOTE_HOST)/evaluate \
		-H "Content-Type: application/json" \
		-d '{"questions":"1. What is React?\n2. How do you use CSS?", "answers":"1. I have 3 years experience.\n2. I use Flexbox and Grid."}' | jq

curl-remote-generate-feedback:
	curl -X POST $(REMOTE_HOST)/generate-feedback \
		-H "Content-Type: application/json" \
		-d '{"candidate_name":"Jane Doe", "job_title":"Designer", "outcome":"rejected", "tone":"friendly"}' | jq
