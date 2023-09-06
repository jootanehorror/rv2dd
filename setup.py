from setuptools import setup, find_packages

with open("../rv2ddd/README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ["ipython>=3.8", "scipy>=1.7.3"]

setup(
    name="rv2dd",
    version="1.0.0",
    author="Oleg Shishkin",
    author_email="os.schischkin@gmail.com",
    description="bivariate discrete distribution based on scipy",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/jootanehorror/rv2dd",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)