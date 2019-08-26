test:
	tox

publish:
	rm -rf dist
	python setup.py sdist bdist_wheel
	twine upload dist/*

generate_rst:
	pandoc --from=markdown --to=rst --output=README.rst README.md
