# -*- coding: UTF-8 -*-
"""setup.py"""

from setuptools import setup
from setuptools import find_packages

with open("README.md", "r") as fin:
    long_description = fin.read()

setup(
    name="scriptd",
    version="0.5.0",
    packages=find_packages(include=["scriptd*"]),

    install_requires=[
        "cryptography>=2.0",
        "flask>=0.12.1",
        "six>=1.9",
        "typing>=3.6.1",
        "requests>=2.0.0"
    ],
    package_data={},
    entry_points={
        "console_scripts": [
            "scriptd = scriptd.cli.server:main",
            "scriptc = scriptd.cli.client:main",
        ]
    },

    # metadata for upload to PyPI
    author="jasonszang",
    author_email="jasonszang@126.com",
    description="Scriptd lets you execute a set of preconfigured scripts or executables via "
                "HTTP API, securely, without exposing terminal access, "
                "and with almost no configurations.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    keywords="",
    url="https://github.com/jasonszang/scriptd",
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ]
)
