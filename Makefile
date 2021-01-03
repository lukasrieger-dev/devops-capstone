setup:
	python3 -m venv .capstone-env
	. .capstone-env/bin/activate

install:
	pip3 install --upgrade pip &&\
		pip3 install -r requirements.txt

test:
	python3 -m pytest -vv --cov=api test/*.py
	#test/test_api_endpoints.py

lint:
	hadolint Dockerfile
	pylint --load-plugins pylint_flask --disable=R,C api/*.py

all: install lint test