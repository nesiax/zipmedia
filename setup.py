"""
zipmedia setup
"""

import os

from setuptools import setup, find_packages

HERE = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(HERE, 'README.txt')) as f:
    README = f.read()
with open(os.path.join(HERE, 'CHANGES.txt')) as f:
    CHANGES = f.read()

REQUIRES = [
    'plaster_pastedeploy',
    'pyramid',
    'pyramid_chameleon',
    'pyramid_debugtoolbar',
    'waitress',
    'alembic',
    'pyramid_retry',
    'pyramid_tm',
    'SQLAlchemy',
    'transaction',
    'zope.sqlalchemy',
    'pyramid_exclog',
    'deform',
    'lingua',
    'Babel',
    'zipstream',
]

# List of dependencies installed via `pip install -e ".[dev]"`
# by virtue of the Setuptools `extras_require` value in the Python
# dictionary below.
DEV_REQUIRES = [
    'pylint',
    'pylint_sqlalchemy',
    'alembic',
    'pytidylib',
    'Paste',
    'faker',
]

TESTS_REQUIRES = [
    'WebTest >= 1.3.1',  # py3 compat
    'pytest >= 3.7.4',
    'pytest-cov',
]

setup(
    name='zipmedia',
    version='0.1',
    description='zipmedia',
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Pyramid',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    ],
    author='Nestor A. Diaz',
    author_email='nestor@tiendalinux.com',
    url='',
    keywords='web pyramid pylons zip media',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    extras_require={
        'testing': TESTS_REQUIRES,
        'dev': DEV_REQUIRES,
    },
    install_requires=REQUIRES,
    entry_points={
        'paste.app_factory': [
            'main = zipmedia:main',
        ],
        'console_scripts': [
            'initialize_zipmedia_db=zipmedia.scripts.initialize_db:main',
        ],
    },
)
