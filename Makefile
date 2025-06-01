ifneq (,$(wildcard .env))
    include .env
    export
endif

update-pip:
	pip freeze > requirements.txt

pytest:
	PYTHONPATH=. pytest

print-env-vars:
	@echo "OPEN_API_KEY=${OPEN_API_KEY}"