setup:
	python -m venv capstone-env
	. capstone-env/bin/activate

install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

test:
	python -m pytest -vv test/test_*.py

lint:
	hadolint Dockerfile
	pylint --load-plugins pylint_flask --disable=R,C ./api/**.py

all: install lint test