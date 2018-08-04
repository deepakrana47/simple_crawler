import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="simple_crawler",
    version="1.0.0a1",
    author="Deepak Singh Rana",
    author_email="deepaksinghrana049@gmail.com",
    description="This is a simple multi requesting crawler",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/deepakrana47/simple_crawler",
    classifiers=(
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    keywords="crawler",
    packages=setuptools.find_packages(),
    install_requires=["requests", "bs4"],
    project_urls={
        "Bug Reports": "https://github.com/deepakrana47/simple_crawler/issues",
        "Source": "https://github.com/deepakrana47/simple_crawler/",
    },
    python_requires=">=2.6",
)