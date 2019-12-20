#!/usr/bin/env python3

from setuptools import find_packages, setup


def readfile(file):
    with open(file) as f:
        return f.read()


def readlines(file):
    return [
        line
        for line in map(str.strip, readfile(file).splitlines())
        if not line.startswith("#")
    ]


setup(
    name="kimsufichecker",
    license="Apache License 2.0",
    author="Sébastien MB",
    author_email="seb@essembeh.org",
    description="Command line tool to monitor Kimsufi plans availability",
    long_description=readfile("README.md"),
    long_description_content_type="text/markdown",
    setup_requires=["setuptools_scm"],
    use_scm_version={"version_scheme": "post-release"},
    install_requires=readlines("requirements.txt"),
    package_dir={"": "src"},
    packages=find_packages("src"),
    entry_points={
        "console_scripts": ["kimsufi-checker = kimsufichecker.__main__:main"]
    },
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
