test:
	nosetests ./tests/

publish:
	python setup.py sdist bdist_wheel upload
