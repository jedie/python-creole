# coding: utf-8

"""
    utils for distutils setup
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    Get README.creole as ReStructuredText on-the-fly for setup.long_description

    More information:
        https://code.google.com/p/python-creole/wiki/UseInSetup

    usage in setup.py e.g.:
    ---------------------------------------------------------------------------
    #!/usr/bin/env python
    # coding: utf-8

    import os
    import sys
    from setuptools import setup, find_packages

    PACKAGE_ROOT = os.path.dirname(os.path.abspath(__file__))

    try:
        from creole.setup_utils import get_long_description
    except ImportError:
        if 'register' in sys.argv or 'sdist' in sys.argv or '--long-description' in sys.argv:
            etype, evalue, etb = sys.exc_info()
            evalue = etype('%s - Please install python-creole >= v0.8 -  e.g.: pip install python-creole' % evalue)
            raise etype, evalue, etb
        long_description = None
    else:
        long_description = get_long_description(PACKAGE_ROOT)

    setup(
        ...
        long_description = long_description,
        ...
    )
    ---------------------------------------------------------------------------

    :copyleft: 2011-2020 by the python-creole team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

import codecs
import os
import shutil
import subprocess
import sys
import warnings
from pathlib import Path

from creole import __version__, creole2html, html2rest
from creole.shared.unknown_tags import raise_unknown_node, transparent_unknown_nodes

RAISE_ERRORS_ARGS = (
    'check', 'register', 'sdist', 'bdist', 'upload',
    '--long-description', '--restructuredtext',
)


def should_raise_errors():
    """
    Raise only errors, if one of RAISE_ERRORS_ARGS is in sys.argv
    or if no argument presents.
    """
    if len(sys.argv) == 1:
        return True

    for arg in RAISE_ERRORS_ARGS:
        if arg in sys.argv:
            return True
    return False


def get_long_description(package_root, filename='README.creole', raise_errors=None):
    """ read README file and convert it on-the-fly to ReStructuredText. """

    warnings.warn('get_long_description() will be removed in the future', DeprecationWarning)

    if raise_errors is None:
        raise_errors = should_raise_errors()

    if raise_errors:
        sys.stderr.write('Test creole2rest and raise an error, if rendering failed...\n')
        # raise a error if a unknown node found
        unknown_emit = raise_unknown_node
    else:
        # ignore unknown nodes
        unknown_emit = transparent_unknown_nodes

    filepath = os.path.join(package_root, filename)
    long_description_origin = ''
    try:
        # Read creole README
        f = codecs.open(filepath, 'r', encoding='utf-8')
        long_description_origin = f.read().strip()
        f.close()

        # convert creole into html
        long_description_html = creole2html(long_description_origin)

        # convert html to ReSt
        long_description_rest = html2rest(
            long_description_html,
            emitter_kwargs={'unknown_emit': unknown_emit}
        )
    except Exception:
        if raise_errors:
            raise
        # Don't raise the error e.g. in ./setup install process
        evalue = sys.exc_info()[1]
        long_description_rest = f'[Error: {evalue}]\n{long_description_origin}'
    else:
        if raise_errors:
            # Test created ReSt code like PyPi does it.
            from creole.rest_tools.pypi_rest2html import pypi_rest2html
            try:
                pypi_rest2html(long_description_rest)
            except SystemExit as e:
                msg = f'Error creole2rest self test failed: rest2html() exist with status code: {e.args[0]}\n'
                sys.stderr.write(msg)
                sys.exit(msg)
            except Exception as e:
                sys.exit(f'ReSt2html error: {e}')
            else:
                if 'check' in sys.argv:
                    print('Generating creole to ReSt to html, ok.')

    return long_description_rest


def update_rst_readme(package_root, filename='README.creole'):
    """
    Generate README.rst from README.creole
    """
    assert isinstance(package_root, Path)
    assert package_root.is_dir(), f'Directory not found: {package_root}'
    creole_readme_path = Path(package_root, filename)
    assert creole_readme_path.is_file(), f'File not found: {creole_readme_path}'

    rest_readme_path = creole_readme_path.with_suffix('.rst')
    print(
        f'Generate {rest_readme_path.name} from {creole_readme_path.name}',
        end='...', flush=True
    )

    with creole_readme_path.open('r') as f:
        creole_readme = f.read().strip()

    # convert creole into html
    html_readme = creole2html(creole_readme)

    # convert html to ReSt
    rest_readme = html2rest(
        html_readme,
        emitter_kwargs={
            'unknown_emit': raise_unknown_node  # raise a error if a unknown node found
        }
    )

    with rest_readme_path.open('w') as f:
        f.write(rest_readme)

    print('done.')


def update_creole_rst_readme():
    update_rst_readme(
        package_root=Path(__file__).parent.parent,
        filename='README.creole'
    )


def verbose_check_output(*args, log=None):
    """ 'verbose' version of subprocess.check_output() """
    call_info = 'Call: %r' % ' '.join(args)
    try:
        output = subprocess.check_output(
            args, universal_newlines=True, stderr=subprocess.STDOUT
        )
    except subprocess.CalledProcessError as err:
        print('\n***ERROR:')
        print(err.output)
        if log is not None:
            log.write(err.output)
        raise
    return call_info, output


def verbose_check_call(*args):
    """ 'verbose' version of subprocess.check_call() """
    print('\tCall: %r\n' % ' '.join(args))
    subprocess.check_call(args, universal_newlines=True)


def confirm(txt):
    print(f'\n{txt}')
    if input('\nPublish anyhow? (Y/N)').lower() not in ('y', 'j'):
        print('Bye.')
        sys.exit(-1)


def poetry_publish(package_root, version, filename='README.creole', log_filename='publish.log'):
    """
    Helper to build and upload to PyPi, with prechecks and update README.rst from README.creole

    Optional arguments are passed to `poetry publish` e.g.:

        $ poetry config repositories.testpypi https://test.pypi.org/simple
        $ poetry run publish --repository=testpypi

    Build and upload to PyPi, if...
        ... __version__ doesn't contains 'dev'
        ... we are on git "master" branch
        ... git repository is 'clean' (no changed files)

    Upload with 'poetry', git tag the current version and git push --tag

    The cli arguments will be pass to 'twine'. So this is possible:
     * Display 'twine' help page...: ./setup.py publish --help
     * use testpypi................: ./setup.py publish --repository=test

    add this to poetry pyproject.toml, e.g.:

        [tool.poetry.scripts]
        publish = 'foo.bar:publish'

    based on:
    https://github.com/jedie/python-code-snippets/blob/master/CodeSnippets/setup_publish.py
    """
    update_rst_readme(package_root=package_root, filename=filename)

    for key in ('dev', 'rc'):
        if key in version:
            confirm(f'WARNING: Version contains {key!r}: v{version}\n')
            break

    print('\nCheck if we are on "master" branch:')
    call_info, output = verbose_check_output('git', 'branch', '--no-color')
    print(f'\t{call_info}')
    if '* master' in output:
        print('OK')
    else:
        confirm(f'\nNOTE: It seems you are not on "master":\n{output}')

    print('\ncheck if if git repro is clean:')
    call_info, output = verbose_check_output('git', 'status', '--porcelain')
    print(f'\t{call_info}')
    if output == '':
        print('OK')
    else:
        print('\n *** ERROR: git repro not clean:')
        print(output)
        sys.exit(-1)

    print('\nRun "poetry check":')
    call_info, output = verbose_check_output('poetry', 'check')
    if 'All set!' not in output:
        print(output)
        confirm('Check failed!')
    else:
        print('OK')

    print('\ncheck if pull is needed')
    verbose_check_call('git', 'fetch', '--all')
    call_info, output = verbose_check_output('git', 'log', 'HEAD..origin/master', '--oneline')
    print(f'\t{call_info}')
    if output == '':
        print('OK')
    else:
        print('\n *** ERROR: git repro is not up-to-date:')
        print(output)
        sys.exit(-1)
    verbose_check_call('git', 'push')

    print('\nCleanup old builds:')

    def rmtree(path):
        path = os.path.abspath(path)
        if os.path.isdir(path):
            print('\tremove tree:', path)
            shutil.rmtree(path)
    rmtree('./dist')
    rmtree('./build')

    print(f'\nSet new version to: v{version}')
    verbose_check_call('poetry', 'version', version)

    print('\nbuild but do not upload...')

    with open(log_filename, 'a') as log:
        log.write('\n')
        log.write('-'*100)
        log.write('\n')
        call_info, output = verbose_check_output('poetry', 'build', log=log)
        print(f'\t{call_info}')
        log.write(call_info)
        log.write(output)

    git_tag = f'v{version}'

    print('\ncheck git tag')
    call_info, output = verbose_check_output(
        'git', 'log', 'HEAD..origin/master', '--oneline',
    )
    if git_tag in output:
        print(f'\n *** ERROR: git tag {git_tag!r} already exists!')
        print(output)
        sys.exit(-1)
    else:
        print('OK')

    print('\nUpload to PyPi via poetry:')
    args = ['poetry', 'publish'] + sys.argv[1:]
    verbose_check_call(*args)

    print('\ngit tag version')
    verbose_check_call('git', 'tag', git_tag)

    print('\ngit push tag to server')
    verbose_check_call('git', 'push', '--tags')

    print(f'Log file is here: {log_filename!r}')
    sys.exit(0)


def publish_python_creole():
    """
        Publish python-creole to PyPi
        Call this via:
            $ poetry run publish
    """
    poetry_publish(
        package_root=Path(__file__).parent.parent,
        version=__version__,
    )


if __name__ == '__main__':
    update_creole_rst_readme()
