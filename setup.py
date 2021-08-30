import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Abrown", # Replace with your own username
    version="1",
    author="Aaron Brown",
    author_email="aaron@probabilitymanagement.orc",
    description="All the SIPmath related functions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/probability-management/PyHDR",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
