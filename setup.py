from setuptools import setup, find_packages

setup(
    name="penny",
    version="0.1.0",
    description="A minimal TUI for coding with LLMs.",
    author="Joseph Blazick",
    author_email="blazickjp@gmail.com",
    url="https://github.com/jblazick/penny",
    packages=find_packages(),
    install_requires=[
        "litellm",
        "textual",
    ],
    entry_points={
        "console_scripts": [
            "penny=src.ChatApp",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
)
