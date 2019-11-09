import warnings

from typeguard import TypeWarning
from typeguard.importhook import install_import_hook


def pytest_addoption(parser):
    group = parser.getgroup('typeguard')
    group.addoption('--typeguard-packages',
                    help='comma separated name list of packages and modules to instrument for '
                         'type checking')
    group.addoption('--typeguard-errors', type='choice', choices=['error', 'warn'],
                    default='error', help='"error" to raise TypeError on a type violation, '
                                          '"warn" to emit TypeWarnings instead')


def pytest_sessionstart(session):
    packages = session.config.getoption('typeguard_packages')
    if packages:
        emit_warnings = session.config.getoption('typeguard_errors') == 'warn'
        if emit_warnings:
            warnings.simplefilter('always', TypeWarning)

        package_list = [pkg.strip() for pkg in packages.split(',')]
        install_import_hook(packages=package_list, emit_warnings=emit_warnings)
