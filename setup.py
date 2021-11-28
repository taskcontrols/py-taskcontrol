# Build the workflow project

from setuptools import setup, Extension, find_packages
import re
import os


# Getting description:
with open("README.md", "r") as fh:
    long_description = fh.read()

# Getting requirements:
with open("requirements.txt") as requirements_file:
    requirements = requirements_file.readlines()

# Getting version:
with open("./taskcontrol/__init__.py") as init_file:
    version = re.search("__version__ = \"(.*?)\"", init_file.read()).group(1)

setup(
    name='taskcontrol',
    version=version,
    scripts=[],
    author="taskcontrols",
    author_email="taskcontrols@gmail.com",
    maintainer="Ganesh B",
    maintainer_email="taskcontrols@gmail.com",
    description="Workflow Automation Library with support for Concurrent or Event based processes or activities in Local or Network Automation Tasks, including CI CD activities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/taskcontrols/taskcontrol",
    download_url="https://pypi.org/project/taskcontrol/",
    packages=find_packages(),
    # package_dir={
    #     # "": "taskcontrol",
    # },
    # package_data={
    #     # "some_dep": ["*.pxd", "*.pyi", "py.typed"],
    # },
    ext_modules=[],
    install_requires=[],
    extras_require={},
    zip_safe=True,
    entry_points={
        'console_scripts': [
            'tasks=run:run'
        ]
    },
    license='Proprietary',
    platforms=["any"],
    keywords=[
        "Automation",
        "CI/CD",
        "CI/CD Automation",
        "DevOps",
        "DevSecOps",
        "Workflow",
        "Workflow Automation",
        "Tasks",
        "Tasks Automation",
        "Workflow Automation",
        "Events Management Library",
        "SQLORM",
        "Database Interface and ORM",
        "Authentication Library",
        "Authorization Library",
        "Socket Server Library",
        "Webhooks Server Library",
        "Client-Agent Architecture Servers Library",
        "Publish-Subscribe Architecture Servers Library",
        "Commands Execution and Automation Library"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        # "License :: OSI Approved :: MIT License",
        "License :: Proprietary"
        "Operating System :: OS Independent"
    ],
)


"""
ext_modules=[
        Extension("dependency_injector.containers",
                ["src/dependency_injector/containers.c"],
                define_macros=list(defined_macros.items()),
                extra_compile_args=["-O2"]),
        Extension("dependency_injector.providers",
                ["src/dependency_injector/providers.c"],
                define_macros=list(defined_macros.items()),
                extra_compile_args=["-O2"]),
    ],
"""

# RUN setup.py with below command
# python3 setup.py sdist bdist_wheel

# The Pypirc file stores the PyPi repository information
# https://docs.python.org/2.5/dist/pypirc.html
# for Windows :  C:\Users\UserName\.pypirc
# for *nix :   ~/.pypirc

# To upload your dist/*.whl file on PyPi https://pypi.org/, use Twine
# python3 -m twine upload dist/*
