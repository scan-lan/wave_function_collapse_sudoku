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

RUN_ONE:=$(shell run_one=$$(ls -rt .benchmarks/**/*.json | tail -n 2 | head -n 1) && run_one=$${run_one##*/} && echo $${run_one:0:4})
RUN_TWO:=$(shell run_two=$$(ls -rt .benchmarks/**/*.json | tail -n 1) && run_two=$${run_two##*/} && echo $${run_two:0:4})
compare-performance:
	pytest-benchmark compare ${RUN_ONE} ${RUN_TWO} --columns='min, mean, iqr, ops, rounds, iterations'
