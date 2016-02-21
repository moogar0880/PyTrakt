.PHONY: clean

init:
	pip install -r requirements.txt

test: clean
	# This runs all of the tests. To run an individual test, run py.test with
	# the -k flag, like "py.test -k test_path_is_not_double_encoded"
	py.test -p no:cacheprovider tests

style:
	flake8 trakt

coverage:
	py.test --verbose --cov-report term --cov=trakt tests

ci: init style test

publish:
	python setup.py register
	python setup.py sdist upload
	rm -fr build dist .egg trakt.egg-info

docs-init:
	pip install -r docs/requirements.txt

clean:
	rm -rf trakt/*.pyc
	rm -rf trakt/__pycache__
	rm -rf tests/__pycache__

docs:
	cd docs && make html
	@echo "\033[95m\n\nBuild successful! View the docs homepage at docs/_build/html/index.html.\n\033[0m"
