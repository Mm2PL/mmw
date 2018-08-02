import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mmw",
    version="1.0",
    author="Maciej Marciniak",
    author_email="jakis128@gmail.com",
    description="This is a library for displaying curses-like windows",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MaciejKtosiowski/mmw",
    packages=setuptools.find_packages(),
    classifiers=(
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3.6",
        "Environment :: Console",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Utilities"
    ),
)