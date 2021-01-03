setup:
	python3 -m venv .capstone-env
	. .capstone-env/bin/activate

install:
	pip3 install --upgrade pip
	pip3 install -r requirements.txt

tests:
	python3 -m pytest -vv test/test_*.py

lint:
	hadolint Dockerfile
	pylint --disable=R,C api/**.py

all: install lint test