"""
XXX
"""

import subprocess
import sys

import check_manifest
import click


def lint_isort(skip, path):
    isort_args = [
        'isort',
        '--recursive',
        '--quiet',
        '--check-only',
        '--multi-line=3',
        '--trailing-comma',
        '--dont-skip=__init__.py',
        path,
    ]
    for item in skip:
        isort_args.append('--skip-glob=' + item)
    isort_result = subprocess.run(args=isort_args)
    if not isort_result.returncode == 0:
        sys.exit(isort_result.returncode)


def lint_check_manifest(skip, path):
    result = check_manifest.check_manifest(path)
    if not result:
        sys.exit(1)


def lint_flake8(skip, path):
    flake8_args = ['flake8', path]
    if skip:
        flake8_args.append('--exclude=' + ','.join(skip))
    flake8_result = subprocess.run(args=flake8_args)
    if not flake8_result.returncode == 0:
        sys.exit(flake8_result.returncode)


def lint_yapf(skip, path) -> None:
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


def lint_vulture(skip, path):
    vulture_args = [
        'vulture',
        '--min-confidence=100',
        path,
    ]
    if skip:
        vulture_args.append('--exclude=' + ','.join(skip))
    vulture_result = subprocess.run(args=vulture_args)
    if not vulture_result.returncode == 0:
        sys.exit(vulture_result.returncode)


def lint_pyroma(skip, path):
    pyroma_args = [
        'pyroma',
        '--min=10',
        path,
    ]
    pyroma_result = subprocess.run(args=pyroma_args)
    if not pyroma_result.returncode == 0:
        sys.exit(pyroma_result.returncode)


@click.command(name='lint')
@click.option('--skip', multiple=True)
def lint(skip) -> None:
    """
    XXX
    """
    path = '.'
    lint_isort(skip=skip, path=path)
    lint_check_manifest(skip=skip, path=path)
    lint_flake8(skip=skip, path=path)
    lint_yapf(skip=skip, path=path)
    lint_vulture(skip=skip, path=path)
    lint_pyroma(skip=skip, path=path)
