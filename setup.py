# Build the workflow project

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='taskcontrol',
     version='1.1.0',
     scripts=[],
     author="Ganesh B",
     author_email="ganeshsurfs@gmail.com",
     description="Create your workflow with order and with before/after middlewares",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/ganeshkbhat/taskcontrol",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent"
     ],
)
