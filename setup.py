import setuptools
import os
import re

def get_abspath(rel_path: str):
    cur = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(cur, rel_path)

# Get long description fron README.md
long_desc = ""
with open(get_abspath("README.md"), "r", encoding="utf-8") as ldf:
    long_desc = ldf.read()

# Get version from __init__.py
version = ""
with open(get_abspath("disbotpy/__init__.py"), "r") as fp:
    # I hate regex so much.
    version = re.search(r"^__version__\s*=\s*['\"]([^'\"]*)['\"]", fp.read(), re.MULTILINE).group(1)

# Get the requirements from requirements.txt
requirements = []
with open(get_abspath("requirements.txt"), "r") as fp:
    requirements = fp.read().splitlines()

# List packages to be included
packages = [
    "disbotpy",
    "disbotpy.types",
]


# Use setuptools.setup to configure the package metadata
setuptools.setup(
    name="disbotpy",
    author="EmreTech",
    version=version,
    description="A completely different approach to Discord API Wrapper libs in Python.",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    url="https://github.com/EmreTech/DisBotPy",
    project_urls = {
        "Bug Tracker": "https://github.com/EmreTech/DisBotPy/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Framework :: AsyncIO",
        "Framework :: aiohttp"
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    packages=packages,
    python_requires=">=3.8.0",
    install_requires=requirements,
)