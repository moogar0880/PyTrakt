PACKAGE=trakt

# TEST_RESULTS defines the directory to which test results will be saved.
TEST_RESULTS=

# LINT_RESULTS defines the directory to which linter results will be saved.
LINT_RESULTS=


.PHONY: ci
ci: init style test

.PHONY: clean
clean:
	rm -rf dist/
	rm -rf build/
	rm -rf $(PACKAGE)/*.pyc
	rm -rf $(PACKAGE)/__pycache__
	rm -rf $(PACKAGE)/__pycache__
	rm -rf $(PACKAGE).egg-info

.PHONY: coverage
coverage:
	py.test --verbose --cov-report term-missing --cov=$(PACKAGE) -p no:cacheprovider tests

.PHONY: docs-init
docs-init:
	pip install -r docs/requirements.txt

.PHONY: docs
docs:
	cd docs && make html
	@echo "\033[95m\n\nBuild successful! View the docs homepage at docs/_build/html/index.html.\n\033[0m"

.PHONY: init
init:
	pip install -r testing-requirements.txt

.PHONY: publish
publish:
	pip install -U pip setuptools wheel twine
	python3 setup.py sdist bdist_wheel
	python3 -m twine upload dist/*
	rm -fr build dist .egg $(PACKAGE).egg-info

.PHONY: style
style:
ifeq ($(strip $(LINT_RESULTS)),)
	flake8 $(PACKAGE)
else
	mkdir -p $(LINT_RESULTS)
	flake8 $(PACKAGE) > $(LINT_RESULTS)/linter.out
endif

.PHONY: test
test: clean
ifeq ($(strip $(TEST_RESULTS)),)
	py.test -s --verbose -p no:cacheprovider tests
else
	mkdir -p $(LINT_RESULTS)
	py.test -s --verbose -p no:cacheprovider tests > $(TEST_RESULTS)/tests.out
endif
