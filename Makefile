init:
	@pip install -r requirements.txt
	@pip install -r requirements-dev.txt

docu:
	@python setup.py build_sphinx

test:
	@python setup.py test

install:
	@python setup.py install
