test:
	pytest

publish:
	python setup.py sdist upload

generate_rst:
	pandoc --from=markdown --to=rst --output=README.rst README.md
