# Make commands for linting

SHELL := /bin/bash -euxo pipefail

.PHONY: fix-yapf
fix-yapf:
	yapf \
		--style='{DEDENT_CLOSING_BRACKETS: true}' \
		--in-place \
		--recursive \
		--exclude='**/_vendor' \
		--exclude='versioneer.py' \
		--exclude='**/_version.py' \
		.

.PHONY: mypy
mypy:
	mypy *.py src/ admin/

.PHONY: pylint
pylint:
	pylint *.py src/ tests/ admin/

.PHONY: shellcheck
shellcheck:
	shellcheck --exclude SC2164,SC1091 admin/*.sh

.PHONY: strictest
strictest:
	strictest lint \
	    --skip='**/_vendor/*' \
	    --skip='versioneer.py' \
	    --skip='**/_version.py' \
	    --src='src'

.PHONY: autoflake
autoflake:
	autoflake \
	    --in-place \
	    --recursive \
	    --remove-all-unused-imports \
	    --remove-unused-variables \
	    --expand-star-imports \
	    --exclude _vendor,src/*/_version.py,versioneer.py,release \
	    .
