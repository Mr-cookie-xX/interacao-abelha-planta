install:
	poetry self update
	poetry install --all-extras

build:
	poetry build

lint:
	poetry run black src
