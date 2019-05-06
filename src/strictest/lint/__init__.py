"""
XXX
"""

import subprocess
import sys

import check_manifest
import click


def lint_isort(skip):
    isort_args = [
        'isort',
        '--recursive',
        '--quiet',
        '--check-only',
        '--multi-line=3',
        '--trailing-comma',
        '--dont-skip=__init__.py',
    ]
    for item in skip:
        isort_args.append('--skip-glob=' + item)
    isort_result = subprocess.run(args=isort_args)
    if not isort_result.returncode == 0:
        sys.exit(isort_result.returncode)


def lint_check_manifest(skip):
    result = check_manifest.check_manifest()
    if not result:
        sys.exit(1)


def lint_flake8(skip):
    flake8_args = ['flake8']
    if skip:
        flake8_args.append('--exclude=' + ','.join(skip))
    flake8_result = subprocess.run(args=flake8_args)
    if not flake8_result.returncode == 0:
        sys.exit(flake8_result.returncode)


def lint_yapf(skip) -> None:
    path = '.'
    yapf_args = [
        'yapf',
        '--style',
        '{DEDENT_CLOSING_BRACKETS: true}',
        '--diff',
        '--recursive',
        path,
    ]
    for item in skip:
        yapf_args.append('--exclude=' + item)
    yapf_result = subprocess.run(args=yapf_args)
    if not yapf_result.returncode == 0:
        sys.exit(yapf_result.returncode)


def lint_vulture(skip):
    pass

@click.command(name='lint')
@click.option('--skip', multiple=True)
def lint(skip) -> None:
    """
    XXX
    """
    lint_isort(skip=skip)
    lint_check_manifest(skip=skip)
    lint_flake8(skip=skip)
    lint_yapf(skip=skip)
    lint_vulture(skip=skip)
