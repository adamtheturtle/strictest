"""
XXX
"""

import subprocess
import sys
import pytest

import click

@click.command(name='lint')
def lint() -> None:
    """
    XXX
    """
    pytest.main(['-s'])
    # isort_args = ['isort', '--recursive', '--check-only', '--multi-line=3', '--trailing-comma']
    # isort_result = subprocess.run(args=isort_args)
    # assert isort_result.returncode == 0:
