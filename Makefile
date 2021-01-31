PACKAGE=trakt

.PHONY: ci
ci: init style test

.PHONY: clean
clean:
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

.PHONY: labels
labels:
	ghlabels -remove -file .github/labels.json

.PHONY: publish
publish:
	pip install -U pip setuptools wheel twine
	python3 setup.py sdist bdist_wheel
	python3 -m twine upload dist/*
	rm -fr build dist .egg $(PACKAGE).egg-info

.PHONY: style
style:
	flake8 $(PACKAGE)

.PHONY: test
test: clean
	py.test -s --verbose -p no:cacheprovider tests
