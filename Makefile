all: run

clean:
	rm -rf venv build dist .pytest_cache .mypy_cache *.egg-info

venv:
	python3 -m venv venv && \
		venv/bin/pip install --upgrade pip setuptools && \
		venv/bin/pip install --editable ".[dev]"

run: venv
	venv/bin/flask --app bob --debug run

format: venv
	venv/bin/black . && venv/bin/isort .

format-check: venv
	venv/bin/black --check . && venv/bin/isort --check .

lint: venv
	venv/bin/flake8 .

mypy: venv
	venv/bin/mypy

test: venv
	venv/bin/pytest

dist: venv format-check lint mypy test
	venv/bin/pip wheel --wheel-dir dist --no-deps .
