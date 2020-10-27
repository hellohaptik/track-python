release:
	python3 setup.py sdist bdist_wheel
	twine upload dist/*

install:
	python3 setup.py sdist bdist_wheel
	pip3 install -e .

.PHONY: release install


