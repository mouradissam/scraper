"""
Copyright (C) 2021-2022 Issam Mourad 

Please see the LICENSE file for the terms and conditions
associated with this software.
"""
import os
import sys

from setuptools import setup
from setuptools import find_packages
from setuptools.command.test import test as TestCommand


def get_long_description():
    """Read the contents of README.md, INSTALL.md files."""
    from os import path

    repo_dir = path.abspath(path.dirname(__file__))
    markdown = []
    for filename in ["README.md", "INSTALL.md"]:
        with open(path.join(repo_dir, filename), encoding="utf-8") as markdown_file:
            markdown.append(markdown_file.read())
    return "\n\n----\n\n".join(markdown)


class Test(TestCommand):
    def run_tests(self):
        import pytest

        errno = pytest.main(["tests/"])
        sys.exit(errno)


setup(
    name="vaper",
    version="0.1",
    author="Issam Mourad",
    description="distributed web crawler",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    license="XFree86",
    keywords=["Google crawler", "Web crawler", "Web scraper"],
    # url="https://github.com/bmoscon/cryptofeed",
    packages=find_packages(exclude=["tests*"]),
    cmdclass={"test": Test},
    python_requires=">=3.7",
    classifiers=[
        "Intended Audience :: Developers",
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Framework :: AsyncIO",
    ],
    tests_require=["pytest"],
    install_requires=[
        "pyyaml",
        "asynctest",
        "asyncio-contextmanager",
        "aiohttp",
        "argparse",
        "asyncio",
    ],
    extras_require={
        "kafka": ["aiokafka>=0.7.0"],
        "mongo": ["motor"],
        "postgres": ["asyncpg"],
        "rabbit": ["aio_pika", "pika"],
        "redis": ["hiredis", "aioredis>=2.0.0"],
        "zmq": ["pyzmq"],
        "all": [
            "aiokafka>=0.7.0",
            "asyncpg",
            "hiredis",
            "aioredis>=2.0.0",
            "pyzmq",
        ],
    },
)
