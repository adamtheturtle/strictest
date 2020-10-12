"""
Tools for linting.
"""

import fnmatch
import subprocess
import sys
from pathlib import Path
from typing import Tuple

import check_manifest
import click
import click_pathlib


def lint_pydocstyle(
    skip: Tuple[str],
    path: Path,
    src: Tuple[Path],
    non_src_package: Tuple[Path],
) -> None:
    """
    Run ``pydocstyle`` and ignore errors.
    We could use the "match" ``pydocstyle`` setting, but this involves regular
    expressions and got too complex.
    """
    ignore_codes = [
        # We do not require summary lines.
        'D200',
        'D205',
        'D400',
        # We don't want blank lines before class docstrings or after the last
        # section in a docstring.
        'D203',
        'D413',
        # We don't need docstrings to start at the first line.
        'D212',
        # Allow blank lines after function docstrings.
        'D202',
        # Section names do not need to end in newlines.
        'D406',
        # Section names do not need dashed underlines.
        'D407',
        # Click uses \b to stop wrapping, so we must allow backslashes in
        # docstrings.
        'D301',
        # We do not care about the imperative mood.
        'D401',
    ]
    args = ['pydocstyle', str(path), '--ignore', ','.join(ignore_codes)]
    pydocstyle_result = subprocess.run(args=args, stdout=subprocess.PIPE)
    lines = pydocstyle_result.stdout.decode().strip().split('\n')
    real_errors = False
    for item_number in range(int(len(lines) / 2)):
        issue_path_and_details = lines[item_number * 2] * 2
        issue = lines[item_number * 2 + 1]
        issue_path_str = issue_path_and_details.split(':')[0]
        issue_path = Path(issue_path_str).relative_to('.')
        location = issue_path_and_details.split(':')[1]
        if not any(
            fnmatch.fnmatch(str(issue_path), skip_pattern)
            for skip_pattern in skip
        ):
            sys.stderr.write(str(issue_path) + '\n')
            sys.stderr.write('\tLine ' + location + '\n')
            sys.stderr.write(issue + '\n')
            real_errors = True

    if real_errors:
        sys.exit(1)


def lint_init_files(
    skip: Tuple[str],
    path: Path,
    src: Tuple[Path],
    non_src_package: Tuple[Path],
) -> None:
    """
    ``__init__`` files exist where they should do.

    If ``__init__`` files are missing, linters may not run on all files that
    they should run on.
    """
    missing_files = set()
    directories = src + non_src_package
    for directory in directories:
        files = directory.glob('**/*.py')
        for python_file in files:
            parent = python_file.parent
            expected_init = parent / '__init__.py'
            if not expected_init.exists():
                if not any(
                    fnmatch.fnmatch(str(python_file), skip_pattern)
                    for skip_pattern in skip
                ):
                    missing_files.add(expected_init)

    if missing_files:
        for expected_init in missing_files:
            message = (
                '`__init__.py` files are expected next to Python files. '
                'The file "{expected_init}" was expected and it does not '
                'exist.\n'
            ).format(expected_init=expected_init)
            sys.stderr.write(message)
    if missing_files:
        sys.exit(1)


def lint_mypy(
    skip: Tuple[str],
    path: Path,
    src: Tuple[Path],
    non_src_package: Tuple[Path],
) -> None:
    """
    Run type checking.
    """
    directories = list(src + non_src_package)
    mypy_args = [
        'mypy',
        '--check-untyped-defs',
        '--disallow-incomplete-defs',
        '--disallow-subclassing-any',
        '--disallow-untyped-calls',
        '--disallow-untyped-defs',
        '--follow-imports=normal',
        '--ignore-missing-imports',
        '--no-implicit-optional',
        '--strict-equality',
        '--strict-optional',
        '--warn-no-return',
        '--warn-redundant-casts',
        '--warn-return-any',
        '--warn-unused-configs',
        '--warn-unused-ignores',
    ] + list(str(item) for item in path.glob('*.py')
             ) + [str(directory) for directory in directories]
    result = subprocess.run(args=mypy_args, stdout=subprocess.PIPE)
    result_lines = result.stdout.decode().strip().split('\n')
    error_lines = []
    for line in result_lines:
        source_file = line.split(':')[0]
        if not any(
            fnmatch.fnmatch(source_file, skip_pattern) for skip_pattern in skip
        ):
            if not line.startswith('Success:'):
                error_lines.append(line)
    print('\n'.join(error_lines))
    if error_lines:
        sys.exit(1)


def lint_isort(
    skip: Tuple[str],
    path: Path,
    src: Tuple[Path],
    non_src_package: Tuple[Path],
) -> None:
    """
    Check for import sort order.
    """
    isort_args = [
        'isort',
        '--recursive',
        '--quiet',
        '--check-only',
        '--multi-line=3',
        '--trailing-comma',
        '--dont-skip=__init__.py',
        str(path),
    ]
    for item in skip:
        isort_args.append('--skip-glob=' + item)
    isort_result = subprocess.run(args=isort_args, stdout=subprocess.PIPE)
    if not isort_result.returncode == 0:
        sys.exit(isort_result.returncode)


def lint_check_manifest(
    skip: Tuple[str],
    path: Path,
    src: Tuple[Path],
    non_src_package: Tuple[Path],
) -> None:
    """
    Check that the manifest file has everything not explicitly ignored.
    """
    result = check_manifest.check_manifest(path)
    if not result:
        sys.exit(1)


def lint_flake8(
    skip: Tuple[str],
    path: Path,
    src: Tuple[Path],
    non_src_package: Tuple[Path],
) -> None:
    """
    Check for formatting issues.
    """
    flake8_args = ['flake8', str(path)]
    if skip:
        flake8_args.append('--exclude=' + ','.join(skip))
    flake8_result = subprocess.run(args=flake8_args, stdout=subprocess.PIPE)
    if not flake8_result.returncode == 0:
        sys.exit(flake8_result.returncode)


def lint_yapf(
    skip: Tuple[str],
    path: Path,
    src: Tuple[Path],
    non_src_package: Tuple[Path],
) -> None:
    """
    Check for formatting issues.
    """
    yapf_args = [
        'yapf',
        '--style',
        '{DEDENT_CLOSING_BRACKETS: true}',
        '--diff',
        '--recursive',
        str(path),
    ]
    for item in skip:
        yapf_args.append('--exclude=' + item)
    yapf_result = subprocess.run(args=yapf_args, stdout=subprocess.PIPE)
    if not yapf_result.returncode == 0:
        sys.exit(yapf_result.returncode)


def lint_vulture(
    skip: Tuple[str],
    path: Path,
    src: Tuple[Path],
    non_src_package: Tuple[Path],
) -> None:
    """
    Check for dead code.
    """
    vulture_args = [
        'vulture',
        '--min-confidence=100',
        str(path),
    ]
    if skip:
        vulture_args.append('--exclude=' + ','.join(skip))
    vulture_result = subprocess.run(args=vulture_args, stdout=subprocess.PIPE)
    if not vulture_result.returncode == 0:
        sys.exit(vulture_result.returncode)


def lint_pyroma(
    skip: Tuple[str],
    path: Path,
    src: Tuple[Path],
    non_src_package: Tuple[Path],
) -> None:
    """
    Check for issues with ``setup.py``.
    """
    pyroma_args = ['pyroma', '--min=10', str(path)]
    pyroma_result = subprocess.run(args=pyroma_args, stdout=subprocess.PIPE)
    if not pyroma_result.returncode == 0:
        sys.exit(pyroma_result.returncode)


def lint_pip_extra_reqs(
    skip: Tuple[str],
    path: Path,
    src: Tuple[Path],
    non_src_package: Tuple[Path],
) -> None:
    """
    Check for extra requirements in ``requirements.txt``.
    """
    pip_extra_reqs_args = [
        'pip-extra-reqs',
        ' '.join([str(item) for item in src]),
    ]
    pip_extra_reqs_result = subprocess.run(
        args=pip_extra_reqs_args,
        stdout=subprocess.PIPE,
    )
    if not pip_extra_reqs_result.returncode == 0:
        sys.exit(pip_extra_reqs_result.returncode)


def lint_pip_missing_reqs(
    skip: Tuple[str],
    path: Path,
    src: Tuple[Path],
    non_src_package: Tuple[Path],
) -> None:
    """
    Check for missing requirements in ``requirements.txt``.
    """
    pip_missing_reqs_args = [
        'pip-missing-reqs',
        ' '.join([str(item) for item in src]),
    ]
    pip_missing_reqs_result = subprocess.run(
        args=pip_missing_reqs_args,
        stdout=subprocess.PIPE,
    )
    if not pip_missing_reqs_result.returncode == 0:
        sys.exit(pip_missing_reqs_result.returncode)


@click.command(name='lint')
@click.option('--skip', multiple=True)
@click.option(
    '--src',
    multiple=True,
    help='Path to src directories',
    type=click_pathlib.Path(
        exists=True,
        dir_okay=True,
        file_okay=False,
        resolve_path=True,
    ),
)
@click.option(
    '--non-src-package',
    multiple=True,
    help='Path to a Python package to lint which is not the source directory',
    type=click_pathlib.Path(
        exists=True,
        dir_okay=True,
        file_okay=False,
        resolve_path=True,
    ),
)
def lint(
    skip: Tuple[str],
    src: Tuple[Path],
    non_src_package: Tuple[Path],
) -> None:
    """
    Run all linters.
    """
    path = Path('.')
    linters = [
        lint_mypy,
        lint_pydocstyle,
        lint_init_files,
        lint_isort,
        lint_check_manifest,
        lint_flake8,
        lint_yapf,
        lint_vulture,
        lint_pyroma,
        lint_pip_extra_reqs,
        lint_pip_missing_reqs,
    ]
    for linter in linters:
        print(linter)
        linter(
            skip=skip,
            path=path,
            src=src,
            non_src_package=non_src_package,
        )
