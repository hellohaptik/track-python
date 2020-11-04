release:
	python3 setup.py clean
	python3 setup.py sdist bdist_wheel
	twine upload --skip-existing dist/*

install:
	python3 setup.py sdist bdist_wheel
	pip3 install -e .

uninstall:
	pip3 uninstall interakt-track-python

.PHONY: release install uninstall


