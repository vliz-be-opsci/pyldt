init:
	@pip install -r requirements.txt
	@pip install -r requirements-dev.txt

docu:
	@python setup.py build_sphinx

test:
	@echo "##### log of make test @ts=$(shell date --iso=seconds)" > pysubyt.log
	@python setup.py test

install:
	@python setup.py install

lint:
	@flake8 --exclude venv --max-line-length=127
