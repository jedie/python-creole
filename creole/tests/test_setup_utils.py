from pathlib import Path

from creole.setup_utils import update_rst_readme
from creole.tests.constants import CREOLE_PACKAGE_ROOT


def test_update_rst_readme(capsys):
    rest_readme_path = update_rst_readme(
        package_root=CREOLE_PACKAGE_ROOT, filename='README.creole'
    )
    captured = capsys.readouterr()
    assert captured.out == 'Generate README.rst from README.creole...nothing changed, ok.\n'
    assert captured.err == ''
    assert isinstance(rest_readme_path, Path)
    assert str(rest_readme_path).endswith('/README.rst')
