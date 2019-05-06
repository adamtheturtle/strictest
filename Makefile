SHELL := /bin/bash -euxo pipefail

include lint.mk


.PHONY: lint
# We do not currently run pydocstyle as we have to ignore vendored items.
lint: \
	strictest \
    mypy \
    pip-extra-reqs \
    pip-missing-reqs \
    pylint \
    pyroma \
    shellcheck \
    vulture

# Fix some linting errors.
.PHONY: fix-lint
fix-lint:
	# Move imports to a single line so that autoflake can handle them.
	# See https://github.com/myint/autoflake/issues/8.
	# Then later we put them back.
	isort --force-single-line --recursive --apply --skip-glob='**/_vendor' --skip-glob='versioneer.py' --skip-glob='**/_version.py'
	$(MAKE) autoflake
	isort --recursive --apply --skip-glob='**/_vendor' --skip-glob='versioneer.py' --skip-glob='**/_version.py'
	$(MAKE) fix-yapf
