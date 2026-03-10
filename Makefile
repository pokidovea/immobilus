lint:
	uv run --python 3.11 --extra dev flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics --extend-exclude=.venv
	uv run --python 3.11 --extra dev flake8 . --count --max-complexity=10 --max-line-length=120 --statistics --extend-exclude=.venv

test:
	uv run --python 3.9 --extra dev pytest
	uv run --python 3.10 --extra dev pytest
	uv run --python 3.11 --extra dev pytest
	uv run --python 3.12 --extra dev pytest
	uv run --python 3.13 --extra dev pytest
	uv run --python 3.14 --extra dev pytest

publish:
	rm -rf dist
	uv build
	uv run --extra dev twine upload dist/*
