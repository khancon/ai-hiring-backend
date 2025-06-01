ifneq (,$(wildcard .env))
    include .env
    export
endif

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
	PYTHONPATH=. pytest

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