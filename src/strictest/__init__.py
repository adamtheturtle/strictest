"""
Linters.
"""

import click

from ._version import get_versions
from .lint import lint
from .fix import fix

_CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(name='strictest', context_settings=_CONTEXT_SETTINGS)
def strictest() -> None:
    """
    XXX
    """
    pass

strictest.add_command(lint)
strictest.add_command(fix)


__version__ = get_versions()['version']  # type: ignore
del get_versions
