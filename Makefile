ifneq (,$(wildcard .env))
    include .env
    export
endif

.PHONY: install update-pip pytest print-env-vars docker-build docker-run docker

install:
	python -m venv venv
	source venv/bin/activate
	pip install -r requirements.txt

clean:
	rm -rf venv
	rm -f requirements.txt

update-pip:
	pip freeze > requirements.txt

pytest:
	PYTHONPATH=. pytest --cov=app --cov-report=term-missing tests/
	coverage html

pytest-ai-routes:
	PYTHONPATH=. pytest tests/test_ai_routes.py

pytest-openai-service:
	PYTHONPATH=. pytest tests/test_openai_service.py

pytest-resume-parser:
	PYTHONPATH=. pytest tests/test_resume_parser.py

print-env-vars:
	@echo "OPEN_API_KEY=${OPEN_API_KEY}"

docker-build:
	docker build -t ai-hiring-backend .

docker-run:
	docker run --env-file .env -p 5000:5000 ai-hiring-backend

docker: docker-build docker-run

flask-run:
	export FLASK_APP=app.py
	export FLASK_ENV=development
	@echo "Running Flask app..."
	flask run

# Makefile API Usage Shortcuts

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
