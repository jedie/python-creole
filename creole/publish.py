from pathlib import Path

from poetry_publish.publish import poetry_publish
from poetry_publish.utils.subprocess_utils import verbose_check_call

import creole


def publish():
    """
        Publish python-creole to PyPi
        Call this via:
            $ poetry run publish
    """
    verbose_check_call('make', 'fix-code-style')  # don't publish if code style wrong

    poetry_publish(
        package_root=Path(creole.__file__).parent.parent,
        version=creole.__version__,
        creole_readme=True  # don't publish if README.rst is not up-to-date
    )
