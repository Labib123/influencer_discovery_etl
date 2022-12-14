from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'A data manipulation package for internal use at ifdb company '
LONG_DESCRIPTION = 'longer description ...'

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="arsenik",
    version=VERSION,
    author="Labib Mansour",
    author_email="labibfunctions@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],  # add any additional packages that
    # needs to be installed along with your package. Eg: 'caer'

    keywords=['python', 'data', 'aws'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: ifdb employees",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System ::   :: Linux",
    ]
)
