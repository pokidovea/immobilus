test:
	pytest

publish:
	python setup.py sdist bdist_wheel upload
