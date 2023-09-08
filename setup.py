import setuptools

setuptools.setup(
    name="redis-cache",
    version="0.0.1",
    author="James White",
    author_email=None,
    description="This package provides a simple python decorator for caching function results in redis.",
    long_description="",
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages("requirements.txt"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
