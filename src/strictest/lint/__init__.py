"""
XXX
"""

import subprocess
import sys

import click


@click.command(name='lint')
@click.option('--skip', multiple=True)
def lint(skip) -> None:
    """
    XXX
    """
    isort_args = [
        'isort',
        '--recursive',
        '--check-only',
        '--multi-line=3',
        '--trailing-comma',
        '--dont-skip=__init__.py'
    ]
    for item in skip:
        isort_args.append(
            '--skip=' + item
        )
    isort_result = subprocess.run(args=isort_args)
    if not isort_result.returncode == 0:
        sys.exit(isort_result.returncode)
