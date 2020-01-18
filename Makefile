SHELL := /bin/bash
MAX_LINE_LENGTH := 119
POETRY_VERSION := $(shell poetry --version 2>/dev/null)

help: ## List all commands
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z0-9 -]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

check-poetry:
	@if [[ "${POETRY_VERSION}" == *"Poetry"* ]] ; \
	then \
		echo "Found version poetry v${POETRY_VERSION}, ok." ; \
	else \
		echo 'Please install poetry first, with e.g.:' ; \
		echo 'make install-poetry' ; \
		exit 1 ; \
	fi

install-poetry: ## install or update poetry
	@if [[ "${POETRY_VERSION}" == *"Poetry"* ]] ; \
	then \
		echo 'Update poetry v$(POETRY_VERSION)' ; \
		poetry self update ; \
	else \
		echo 'Install poetry' ; \
		curl -sSL "https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py" | python3 ; \
	fi

install: check-poetry ## install python-creole via poetry
	poetry install

lint: ## Run code formatters and linter
# 	poetry run isort --check-only --recursive creole
# 	poetry run black --line-length=119 --check creole
	poetry run flake8 creole

fix-code-style: ## Fix code formatting
# 	poetry run flynt --line_length=119 creole
# 	poetry run isort --apply --recursive creole
	poetry run autopep8 --ignore-local-config --max-line-length=${MAX_LINE_LENGTH} --aggressive --aggressive --in-place --recursive creole

tox-listenvs: check-poetry ## List all tox test environments
	poetry run tox --listenvs

tox: check-poetry ## Run pytest via tox with all environments
	poetry run tox

tox-py36: check-poetry ## Run pytest via tox with *python v3.6*
	poetry run tox -e py36

tox-py37: check-poetry ## Run pytest via tox with *python v3.7*
	poetry run tox -e py37

tox-py38: check-poetry ## Run pytest via tox with *python v3.8*
	poetry run tox -e py38

pytest: check-poetry ## Run pytest
	poetry run pytest

release: ## Release new version [usage: v=rule]
	# Update pyproject and changelog
	poetry version $(v)
	sed -i "" "s/\[Unreleased\]/\[$(VERSION)\] - $(shell date +%F)/" CHANGELOG.md
	# Create commit and tag
	git commit pyproject.toml CHANGELOG.md -m "Bump version to $(VERSION)" && git tag "v$(VERSION)"
	git push && git push --tags
	# Publish to pypi
	poetry publish --build


.PHONY: help install lint fix test release