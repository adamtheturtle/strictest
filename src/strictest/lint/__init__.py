"""
XXX
"""

import subprocess
import sys

import click


@click.command(name='lint')
def lint() -> None:
    """
    XXX
    """
    isort_args = ['isort', '--recursive', '--check-only']
    isort_result = subprocess.run(args=isort_args)
    if not isort_result.returncode == 0:
        sys.exit(isort_result.returncode)
