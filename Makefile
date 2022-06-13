requirements:
	pip install -r requirements/base.txt

test-requirements:
	pip install -r requirements/test.txt

test:
	pytest
