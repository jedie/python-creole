from pathlib import Path

from poetry_publish.publish import poetry_publish

import creole


def publish():
    """
        Publish python-creole to PyPi
        Call this via:
            $ poetry run publish
    """
    poetry_publish(
        package_root=Path(creole.__file__).parent.parent,
        version=creole.__version__,
    )
