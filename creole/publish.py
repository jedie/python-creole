from pathlib import Path

import creole
from creole.setup_utils import update_creole_rst_readme
from poetry_publish.publish import poetry_publish


def publish():
    """
        Publish python-creole to PyPi
        Call this via:
            $ poetry run publish
    """
    update_creole_rst_readme()  # don't publish if README.rst is not up-to-date
    poetry_publish(
        package_root=Path(creole.__file__).parent.parent,
        version=creole.__version__,
    )
