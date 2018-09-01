# -*- coding: UTF-8 -*-
"""setup.py"""

from setuptools import setup
from setuptools import find_packages

setup(
    name="scriptd",
    version="0.1.0",
    packages=find_packages(),

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
    description="",
    license="BSD 2-Clause",
    keywords="",
    url="",  # project home page, if any
)