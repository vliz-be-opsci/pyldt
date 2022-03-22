SHELL := /bin/bash
PYTHON = python3
TEST_PATH = ./tests/
FLAKE8_EXCLUDE = venv,.venv,.eggs,.tox,.git,__pycache__,*.pyc

clean:
	@find . -name '*.pyc' -exec rm --force {} +
	@find . -name '*.pyo' -exec rm --force {} +
	@find . -name '*~' -exec rm --force {} +
	@rm -rf build
	@rm -rf dist
	@rm -rf *.egg-info
	@rm -f *.sqlite
	@rm -rf .cache

init:
	@pip install --upgrade pip
	@pip install -e .
	#@pip install -r requirements.txt -U   #we need this explicit variant wheb using unreleased -e dependencies - to keep automatic testing happy

init-dev: init
	@pip install -e .[dev]

docu:
	@${PYTHON} setup.py build_sphinx

test:
	@${PYTHON} -m pytest ${TEST_PATH} --disable-warnings

check:
	@${PYTHON} -m flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics --exclude ${FLAKE8_EXCLUDE}
	@${PYTHON} -m flake8 . --count --exit-zero --max-complexity=10 --max-line-length=132 --statistics --exclude ${FLAKE8_EXCLUDE}

install:
	@${PYTHON} setup.py install

docker-build:
	@docker build . -t pysubyt
