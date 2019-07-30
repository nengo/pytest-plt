#!/usr/bin/env python
import imp
import io
import os
import sys

from setuptools import find_packages, setup


def read(*filenames, **kwargs):
    encoding = kwargs.get("encoding", "utf-8")
    sep = kwargs.get("sep", "\n")
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


root = os.path.dirname(os.path.realpath(__file__))
version_module = imp.load_source(
    "version", os.path.join(root, "pytest_plt", "version.py"))
testing = "test" in sys.argv or "pytest" in sys.argv

install_requires = [
    "matplotlib",
    "pytest",
]
docs_require = [
    "nengo_sphinx_theme",
    "sphinx",
]
checks_require = [
    "codespell",
    "flake8",
    "gitlint",
    "pylint",
]
tests_require = [
    "coverage>=4.3",
]


setup(
    name="pytest-plt",
    version=version_module.version,
    author="Applied Brain Research",
    author_email="info@appliedbrainresearch.com",
    packages=find_packages(),
    scripts=[],
    data_files=[],
    url="https://github.com/nengo/pytest-plt",
    license="MIT license",
    description="Fixtures for quickly making Matplotlib plots in tests",
    long_description=read("README.rst", "CHANGES.rst"),
    setup_requires=install_requires,
    install_requires=install_requires,
    extras_require={
        "all": docs_require + checks_require + tests_require,
        "checks": checks_require,
        "docs": docs_require,
        "tests": tests_require,
    },
    tests_require=tests_require,
    python_requires=">=3.5",
    entry_points={
        "pytest11": ["plt = pytest_plt.plugin"],
    },
    classifiers=[
        # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 5 - Production/Stable",
        "Framework :: Pytest",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
