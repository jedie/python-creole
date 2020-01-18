.PHONY: help install lint fix test release

VERSION := $$(poetry version | sed -n 's/contxt-sdk //p')

help: ## List all commands
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z -]+:.*?## / {printf "\033[36m%-10s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install:
	pip install poetry
	poetry install

lint: ## Run code formatters and linter
	poetry run isort --check-only --recursive creole
	poetry run black --line-length=119 --check creole
	poetry run flake8 creole

fix: ## Fix code formatting
	poetry run flynt --line_length=119 creole
	poetry run isort --apply --recursive creole
	poetry run black --line-length=119 creole

test: ## Run unit tests
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