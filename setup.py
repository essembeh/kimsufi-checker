#!/usr/bin/env python3

from setuptools import setup


def readfile(file):
    with open(file) as f:
        return f.read()


setup(
    name="kimsufichecker",
    license="Apache License 2.0",
    author="Sébastien MB",
    author_email="seb@essembeh.org",
    description="Command line tool to monitor Kimsufi plans availability",
    long_description=readfile("README.md"),
    long_description_content_type="text/markdown",
    use_scm_version={"version_scheme": "post-release"},
    setup_requires=["setuptools_scm"],
    install_requires=["pytput"],
    package_dir={"": "src"},
    packages=["kimsufichecker"],
    entry_points={"console_scripts": ["kimsufi-checker = kimsufichecker.__main__:main"]},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
