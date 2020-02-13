"""
    :copyleft: 2020 by python-creole team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""
import os
import shutil
import subprocess
from pathlib import Path

from creole import __version__
from creole.setup_utils import assert_rst_readme
from creole.tests.constants import CREOLE_PACKAGE_ROOT


def assert_file_contains_string(file_path, string):
    with file_path.open('r') as f:
        for line in f:
            if string in line:
                return
    raise AssertionError(f'File {file_path} does not contain {string!r} !')


def test_version():
    if 'dev' not in __version__ and 'rc' not in __version__:
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


def test_assert_rst_readme():
    assert_rst_readme(package_root=CREOLE_PACKAGE_ROOT)


def test_poetry_check():
    poerty_bin = shutil.which('poetry')

    output = subprocess.check_output(
        [poerty_bin, 'check'],
        universal_newlines=True,
        env=os.environ,
        stderr=subprocess.STDOUT,
        cwd=str(CREOLE_PACKAGE_ROOT),
    )
    print(output)
    assert output == 'All set!\n'
