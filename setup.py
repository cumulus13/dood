import io
from setuptools import setup, find_packages
import shutil
import os
import sys

NAME = "dood"

shutil.copy2('__version__.py', NAME)

# Read the README file
with io.open("README.md", "rt", encoding="utf8") as f:
    readme = f.read()

# Read the version from idm/__version__.py
version = {}
with open(os.path.join(NAME, "__version__.py")) as fp:
    exec(fp.read(), version)
version = version['version']

# Determine the packages based on the extra provided
extra_packages = [NAME]

install_requires = [
        'argparse',
        'rich', 
        'pydebugger',
        'bs4', 
        'requests', 
    ]

if sys.platform == 'win32':
    install_requires.append('idm')

setup(
    name=NAME,
    version=version,
    url="https://github.com/cumulus13/dood",
    project_urls={
        "Documentation": "https://github.com/cumulus13/dood",
        "Code": "https://github.com/cumulus13/dood",
    },
    license="GPL",
    author="Hadi Cahyadi LD",
    author_email="cumulus13@gmail.com",
    maintainer="cumulus13 Team",
    maintainer_email="cumulus13@gmail.com",
    description="Dood link Generator",
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=install_requires,
    entry_points={
        "console_scripts": [
            "dood = dood.__main__:usage",
        ]
    },
    data_files=['__version__.py', 'README.md'],
    license_files=["LICENSE.rst"],    
    include_package_data=True,
    python_requires=">=2.7",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        'License :: OSI Approved :: GNU General Public License (GPL)', 
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
    ],
)
