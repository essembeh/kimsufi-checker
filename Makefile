.PHONY: install

all: 

venv: requirements.txt requirements-dev.txt 
	virtualenv -p python3 venv --no-site-packages
	./venv/bin/pip install -r requirements.txt
	./venv/bin/pip install -r requirements-dev.txt
	touch venv

install:
	test -n "$(VIRTUAL_ENV)"
	pip install -e .
