include .env

update-pip:
	pip freeze > requirements.txt

pytest:
	PYTHONPATH=. pytest