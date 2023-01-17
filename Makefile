# Terminal Colours
RED?=$(shell tput setaf 1)
GREEN?=$(shell tput setaf 2)
YELLOW?=$(shell tput setaf 3)
BLUE?=$(shell tput setaf 4)
BOLD?=$(shell tput bold)
RST?=$(shell tput sgr0)

##@ Clean
.PHONY: clean
clean: clean-pyc clean-build ## Delete all artifacts

.PHONY: clean-pyc
clean-pyc: ## Delete Python cache artifacts
	@find . -name '*.pyc' -delete
	@find . -name '*.pyo' -delete
	@find . -name __pycache__ -delete

.PHONY: clean-build
clean-build: ## Delete distribution artifacts
	@rm --force --recursive build dist *.egg-info doc/build doc/man/*.1

##@ Build
.PHONY: build
build: sdist wheel ## Build sdist & wheel

.PHONY: wheel
wheel: manpages ## Build wheel with the build module
	@python -m build --no-isolation --wheel

.PHONY: sdist
sdist: manpages ## Build sdist with the build module
	@python -m build --no-isolation --sdist

# requires library to be built & installed due to
# sphinx's introspection into the library
.PHONY: docs
docs: ## Build html documentation with Sphinx
	make -C doc

.PHONY: manpages
manpages: ## Build manpages using scdoc
	make -C doc/man

##@ Utilities
.DEFAULT_GOAL = help
.PHONY: help
help: ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  $(YELLOW)make$(RST) $(BLUE)command$(RST)\n"} /^[a-zA-Z0-9_-]+:.*?##/ { printf "  $(BLUE)%-15s$(RST) %s\n", $$1, $$2 } /^##@/ { printf "\n$(BOLD)%s$(RST)\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

.PHONY: test
test: ## Run all tests with pytest
	@pytest -v

.PHONY: reuse
reuse: ## Validate licensing information with reuse
	@reuse lint

.PHONY: ruff
ruff: ## Lint source code with ruff
	@ruff mididings tests

.PHONY: mdl
mdl: ## Lint all markdown documentation with mdl
	@mdl .
