"""
XXX
"""

import subprocess
import sys
from pathlib import Path

import check_manifest
import click
import click_pathlib


def lint_init_files(skip, path, src) -> None:
    """
    ``__init__`` files exist where they should do.

    If ``__init__`` files are missing, linters may not run on all files that
    they should run on.
    """
    for directory in src:
        files = directory.glob('**/*.py')
        for python_file in files:
            parent = python_file.parent
            expected_init = parent / '__init__.py'
            assert expected_init.exists()


def lint_isort(skip, path, src):
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


def lint_check_manifest(skip, path, src):
    result = check_manifest.check_manifest(path)
    if not result:
        sys.exit(1)


def lint_flake8(skip, path, src):
    flake8_args = ['flake8', path]
    if skip:
        flake8_args.append('--exclude=' + ','.join(skip))
    flake8_result = subprocess.run(args=flake8_args)
    if not flake8_result.returncode == 0:
        sys.exit(flake8_result.returncode)


def lint_yapf(skip, path, src) -> None:
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


def lint_vulture(skip, path, src):
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


def lint_pyroma(skip, path, src):
    pyroma_args = [
        'pyroma',
        '--min=10',
        path,
    ]
    pyroma_result = subprocess.run(args=pyroma_args)
    if not pyroma_result.returncode == 0:
        sys.exit(pyroma_result.returncode)


def lint_pip_extra_reqs(skip, path, src):
    """
    XXX
    """
    pip_extra_reqs_args = [
        'pip-extra-reqs',
        ' '.join([str(item) for item in src]),
    ]
    pip_extra_reqs_result = subprocess.run(args=pip_extra_reqs_args)
    if not pip_extra_reqs_result.returncode == 0:
        sys.exit(pip_extra_reqs_result.returncode)


def lint_pip_missing_reqs(skip, path, src):
    """
    XXX
    """
    pip_missing_reqs_args = [
        'pip-missing-reqs',
        ' '.join([str(item) for item in src]),
    ]
    pip_missing_reqs_result = subprocess.run(args=pip_missing_reqs_args)
    if not pip_missing_reqs_result.returncode == 0:
        sys.exit(pip_missing_reqs_result.returncode)


@click.command(name='lint')
@click.option('--skip', multiple=True)
@click.option(
    '--src',
    multiple=True,
    default=('src', ),
    help='Path to src directories',
    type=click_pathlib.Path(
        exists=True,
        dir_okay=True,
        file_okay=False,
        resolve_path=True,
    ),
)
def lint(skip, src) -> None:
    """
    XXX
    """
    path = '.'
    lint_init_files(skip=skip, path=path, src=src)
    # lint_isort(skip=skip, path=path, src=src)
    # lint_check_manifest(skip=skip, path=path, src=src)
    # lint_flake8(skip=skip, path=path, src=src)
    # lint_yapf(skip=skip, path=path, src=src)
    # lint_vulture(skip=skip, path=path, src=src)
    # lint_pyroma(skip=skip, path=path, src=src)
    # lint_pip_extra_reqs(skip=skip, path=path, src=src)
    # lint_pip_missing_reqs(skip=skip, path=path, src=src)
