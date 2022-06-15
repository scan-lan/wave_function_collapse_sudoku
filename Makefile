requirements-base:
	pip install -r requirements/base.txt

requirements-test: requirements-base
	pip install -r requirements/test.txt

lint:
	flake8

lint-fix:
	autopep8 -iraa main.py logic ui util --max-line-length 120

test:
	pytest --benchmark-skip

test-performance:
	pytest --benchmark-only --benchmark-autosave --benchmark-columns='min, mean, median, iqr, outliers, ops, rounds, iterations'

test-performance-no-save:
	pytest -s --benchmark-only --benchmark-columns='min, mean, iqr, ops, rounds, iterations'

