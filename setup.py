# Build the workflow project

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='taskcontrol',
    version='1.3.0-beta',
    scripts=[],
    author="taskcontrols",
    author_email="taskcontrols@gmail.com",
    description="Workflow Automation Library with support for Concurrent or Event based processes or activities in Local or Network Automation Tasks, including CI CD activities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/taskcontrols/taskcontrol",
    packages=setuptools.find_packages(),
    install_requires=[
    ],
    entry_points={
        'console_scripts': [
            'tasks=run:run'
        ]
    },
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
)

# RUN setup.py with below command
# python3 setup.py sdist bdist_wheel

# The Pypirc file stores the PyPi repository information
# https://docs.python.org/2.5/dist/pypirc.html
# for Windows :  C:\Users\UserName\.pypirc
# for *nix :   ~/.pypirc

# To upload your dist/*.whl file on PyPi https://pypi.org/, use Twine
# python3 -m twine upload dist/*
