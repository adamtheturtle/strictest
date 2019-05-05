"""
Linters.
"""

import click

from ._version import get_versions

_CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(name='strictest', context_settings=_CONTEXT_SETTINGS)
def strictest() -> None:
    pass


__version__ = get_versions()['version']  # type: ignore
del get_versions
