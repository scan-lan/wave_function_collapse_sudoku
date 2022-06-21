requirements-base:
	poetry install --no-dev

requirements-dev:
	poetry install
	poetry run pre-commit install

lint:
	poetry run flake8

lint-fix:
	poetry run black .

test: requirements-dev
	poetry run pytest -m "not performance and not success_rate and not slow"

test-slow: requirements-dev
	poetry run pytest -m "not performance and not success_rate"

BENCHMARK_COLUMNS:=$(shell echo "'mean, min, ops, rounds, iterations'")
BENCHMARK_SORT:=$(shell echo "'mean'")

test-performance: requirements-dev
	poetry run pytest -m performance --benchmark-autosave --benchmark-columns=${BENCHMARK_COLUMNS} --benchmark-sort=${BENCHMARK_SORT}

test-performance-no-save: requirements-dev
	poetry run pytest -m performance --benchmark-only --benchmark-columns=${BENCHMARK_COLUMNS} --benchmark-sort=${BENCHMARK_SORT}

RUN_ONE:=$(shell run_one=$$(ls -rt .benchmarks/**/*.json | tail -n 2 | head -n 1) && run_one=$${run_one##*/} && echo $${run_one:0:4})
RUN_TWO:=$(shell run_two=$$(ls -rt .benchmarks/**/*.json | tail -n 1) && run_two=$${run_two##*/} && echo $${run_two:0:4})

compare-last-two-performances: requirements-dev
	poetry run pytest-benchmark compare ${RUN_ONE} ${RUN_TWO} --columns=${BENCHMARK_COLUMNS} --sort=${BENCHMARK_SORT}

test-success-rates:
	poetry run pytest -m success_rate

run:
	poetry run python main.py
