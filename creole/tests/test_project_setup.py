"""
    :copyleft: 2020 by python-creole team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

from pathlib import Path

from creole import __version__
from creole.tests.constants import CREOLE_PACKAGE_ROOT


def assert_file_contains_string(file_path, string):
    with file_path.open('r') as f:
        for line in f:
            if string in line:
                return
    raise AssertionError(f'File {file_path} does not contain {string!r} !')


def test_version():
    if 'dev' not in __version__:
        version_string = f'v{__version__}'

        assert_file_contains_string(
            file_path=Path(CREOLE_PACKAGE_ROOT, 'README.creole'),
            string=version_string
        )

        assert_file_contains_string(
            file_path=Path(CREOLE_PACKAGE_ROOT, 'README.rst'),
            string=version_string
        )

    assert_file_contains_string(
        file_path=Path(CREOLE_PACKAGE_ROOT, 'pyproject.toml'),
        string=f'version = "{__version__}"'
    )
