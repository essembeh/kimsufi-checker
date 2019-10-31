.PHONY: install publish clean flake8

all: clean flake8

venv: requirements.txt
	virtualenv -p python3 venv --no-site-packages
	./venv/bin/pip install -r requirements.txt
	touch venv

clean:
	rm -rf flake-report dist/ build/

flake8: venv
	flake8 src/

install: venv
	test -n "$(VIRTUAL_ENV)"
	pip install -e .

publish: venv
	test -n "$(VIRTUAL_ENV)"
	python3 setup.py sdist bdist_wheel
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*
