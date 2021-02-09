"""setuptools script to install sarctransform"""
from __future__ import unicode_literals

# based on https://github.com/pypa/sampleproject/blob/3b73bd9433d031f0873a6cbc5bd04cea2e3407cb/setup.py
# which is linked from https://packaging.python.org/guides/distributing-packages-using-setuptools/#setup-py

from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README file
with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

# copied from https://github.com/pypa/pip/blob/edda92720385d55e7600019bfe96e2f325b58fcc/setup.py#L11
# and https://packaging.python.org/guides/single-sourcing-package-version/
def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    # intentionally *not* adding an encoding option to open, See:
    #   https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    with codecs.open(os.path.join(here, rel_path), "r") as fp:
        return fp.read()


# copied from https://github.com/pypa/pip/blob/edda92720385d55e7600019bfe96e2f325b58fcc/setup.py#L11
# and https://packaging.python.org/guides/single-sourcing-package-version/
def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            # __version__ = "0.9"
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    name="sarctransform",
    version=get_version("__init__.py"),
    description="sarctransform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={"": "."},
    packages=[""],  # find_packages(where='.'),  # Required
    python_requires=">=3.2, <4",
    # This field lists other packages that your project depends on to run.
    # Any package you put here will be installed by pip when your project is
    # installed, so they must be valid existing projects.
    #
    # For an analysis of "install_requires" vs pip's requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=[
        "dbf ~= 0.99.0",
        "dbfread ~= 2.0.7",
        "xlrd ~= 2.0.1",
        # "google-cloud-bigquery ~= 2.3.1",
        # "googleads ~= 26.0.0",
        # "pandas ~= 1.0.0",
        # "jinja2",
        # "pymysql",
        # "python-dateutil",
    ],
    # List additional groups of dependencies here (e.g. development
    # dependencies). Users will be able to install these using the "extras"
    # syntax, for example:
    #
    #   $ pip install sampleproject[dev]
    #
    # Similar to `install_requires` above, these must be valid existing
    # projects.
    extras_require={  # Optional
        "dev": [],
        "test": [],
    },
    # If there are data files included in your packages that need to be
    # installed, specify them here.
    package_data={},  # Optional
    data_files=[],  # Optional
    # https://setuptools.readthedocs.io/en/latest/setuptools.html#automatic-script-creation
    entry_points={  # Optional
        "console_scripts": [
            "sarctransform = sarctransform:main",
        ],
    },
    # project_urls={}  # Optional
)
