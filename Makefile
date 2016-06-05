PACKAGE=trakt

.PHONY: clean

init:
	pip install -r testing-requirements.txt

test: clean
	py.test -s --verbose -p no:cacheprovider tests

style:
	flake8 trakt

coverage:
	py.test --verbose --cov-report term-missing --cov=$(PACKAGE) -p no:cacheprovider tests

ci: init style test

publish:
	python setup.py register
	python setup.py sdist upload
	rm -fr build dist .egg $(PACKAGE).egg-info

docs-init:
	pip install -r docs/requirements.txt

clean:
	rm -rf $(PACKAGE)/*.pyc
	rm -rf $(PACKAGE)/__pycache__
	rm -rf $(PACKAGE)/__pycache__
	rm -rf $(PACKAGE).egg-info

docs:
	cd docs && make html
	@echo "\033[95m\n\nBuild successful! View the docs homepage at docs/_build/html/index.html.\n\033[0m"
