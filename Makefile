PACKAGE=trakt

.PHONY: ci clean coverage docs-init docs init labels publish style test

ci: init style test

clean:
	rm -rf $(PACKAGE)/*.pyc
	rm -rf $(PACKAGE)/__pycache__
	rm -rf $(PACKAGE)/__pycache__
	rm -rf $(PACKAGE).egg-info

coverage:
	py.test --verbose --cov-report term-missing --cov=$(PACKAGE) -p no:cacheprovider tests

docs-init:
	pip install -r docs/requirements.txt

docs:
	cd docs && make html
	@echo "\033[95m\n\nBuild successful! View the docs homepage at docs/_build/html/index.html.\n\033[0m"

init:
	pip install -r testing-requirements.txt

labels:
	ghlabels -remove -file .github/labels.json

publish:
	python setup.py register
	python setup.py sdist upload
	rm -fr build dist .egg $(PACKAGE).egg-info

style:
	flake8 $(PACKAGE)

test: clean
	py.test -s --verbose -p no:cacheprovider tests
