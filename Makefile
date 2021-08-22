APPLICATION_MODULE=src/alfred
TEST_MODULE=tests

.PHONY: activate
activate: ## activate the virtualenv associate with this project
	pipenv shell

.PHONY: ci
ci : lint tests ## run continuous integration process

.PHONY: coverage
coverage: coverage_run coverage_html ## output the code coverage in htmlcov/index.html

coverage_run :
	pipenv run coverage run -m unittest discover $(TEST_MODULE)

coverage_html:
	pipenv run coverage html
	@echo "$ browse htmlcov/index.html"

.PHONY: clean
clean : ## remove all transient directories and files
	rm -rf dist
	rm -f .coverage
	rm -rf *.egg-info
	rm -f MANIFEST
	find -name __pycache__ -print0 | xargs -0 rm -rf
	pipenv --rm

.PHONY: dist
dist:
	pipenv run python setup.py bdist sdist

# @see http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
.DEFAULT_GOAL := help
.PHONY: help
help: ## provides cli help for this makefile (default)
	@grep -E '^[a-zA-Z_0-9-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: install_requirements_dev
install_requirements_dev: ## install pip requirements for development
	pipenv install --dev

.PHONY: install_requirements
install_requirements: ## install pip requirements based on requirements.txt
	pipenv install

.PHONY: lint
lint: ## run pylint
	pipenv run pylint --rcfile=.pylintrc $(APPLICATION_MODULE)

.PHONY: tests
tests: tests_units tests_acceptances  ## run automatic tests

.PHONY: tests_units
tests_units: ## run only unit tests
	pipenv run python -u -m unittest discover "$(TEST_MODULE)/units"

.PHONY: tests_acceptances
tests_acceptances: ## run only unit tests
	pipenv run python -u -m unittest discover "$(TEST_MODULE)/acceptances"

.PHONY: twine
twine: ## publish on pypi
	$(MAKE) dist
	pipenv run twine upload dist/*

.PHONY: update_requirements
update_requirements: ## update the project dependencies based on setup.py declaration
	pipenv update
