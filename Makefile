PROJECT = yzconfig

PYTHON_VERSION = 2.7
REQUIREMENTS = requirements.txt
VIRTUAL_ENV := .venv$(PYTHON_VERSION)
PYTHON := $(VIRTUAL_ENV)/bin/python

test:
	$(PYTHON) -m unittest $(PROJECT).tests

test_coverage: test
	$(info No no coverage yet)


venv_init:
	if [ ! -d $(VIRTUAL_ENV) ]; then \
		virtualenv -p python$(PYTHON_VERSION) --prompt="($(PROJECT):$(PYTHON_VERSION)) " $(VIRTUAL_ENV); \
	fi

venv:  venv_init
	$(VIRTUAL_ENV)/bin/pip install -r $(REQUIREMENTS)

clean_venv:
	rm -rf $(VIRTUAL_ENV)

clean_pyc:
	find . -name \*.pyc -delete

clean: clean_venv clean_pyc

package:
	$(PYTHON) setup.py sdist
