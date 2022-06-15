requirements-base:
	pip install -r requirements/base.txt

requirements-test: requirements-base
	pip install -r requirements/test.txt

lint:
	flake8

lint-fix:
	autopep8 -iraa main.py logic ui util --max-line-length 120

test:
	pytest
