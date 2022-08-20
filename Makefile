SHELL := /bin/bash
MAX_LINE_LENGTH := 119
POETRY_VERSION := $(shell poetry --version 2>/dev/null)

help: ## List all commands
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z0-9 -]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

check-poetry:
	@if [[ "${POETRY_VERSION}" == *"Poetry"* ]] ; \
	then \
		echo "Found ${POETRY_VERSION}, ok." ; \
	else \
		echo 'Please install poetry first, with e.g.:' ; \
		echo 'make install-poetry' ; \
		exit 1 ; \
	fi

install-poetry:  ## install or update poetry
	pip3 install -U pip
	pip3 install -U poetry

install: check-poetry ## install python-creole via poetry
	poetry install

update: install-poetry ## Update the dependencies as according to the pyproject.toml file
	poetry update -v

lint: ## Run code formatters and linter
	poetry run darker --diff --check
	poetry run isort --check-only .

fix-code-style: ## Fix code formatting
	poetry run darker
	poetry run autopep8 --in-place --max-line-length ${MAX_LINE_LENGTH} --recursive .
	poetry run darker
	poetry run isort .

tox-listenvs: check-poetry ## List all tox test environments
	poetry run tox --listenvs

tox: check-poetry ## Run pytest via tox with all environments
	poetry run tox

pytest: check-poetry ## Run pytest
	poetry run pytest

update-readmes: ## update README.rst and README.md from README.creole
	poetry run update_rst_readme
	poetry run update_markdown_readme

publish: ## Release new version to PyPi
	poetry run publish


.PHONY: help install lint fix test publish