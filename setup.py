from setuptools import setup, find_packages

setup(
    name="penny",
    version="0.1.0",
    description="A CLI tool for working with LLMs.",
    author="Joseph Blazick",
    author_email="joe.blazick@yahoo.com",
    url="https://github.com/jblazick/penny",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "numpy",
        "openai",
        "click",
        "pydantic",
        "pyyaml",
        "instructor",
    ],
    entry_points={
        "console_scripts": [
            "penny=src.penny:penny",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
)
