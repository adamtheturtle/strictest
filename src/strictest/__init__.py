"""
Linters.
"""

import click

from ._version import get_versions
from .fix import fix
from .lint import lint

_CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(name='strictest', context_settings=_CONTEXT_SETTINGS)
def strictest() -> None:
    """
    XXX
    """


strictest.add_command(lint)
strictest.add_command(fix)

__version__ = get_versions()['version']  # type: ignore
del get_versions
