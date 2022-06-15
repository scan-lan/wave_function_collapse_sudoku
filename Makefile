requirements-base:
	pip install -r requirements/base.txt

requirements-test: requirements-base
	pip install -r requirements/test.txt

lint:
	flake8

lint-fix:
	autopep8 -ira main.py logic ui util

test:
	pytest
