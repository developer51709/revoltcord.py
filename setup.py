from setuptools import setup, find_packages

setup(
    name="revoltcord.py",
    version="0.1.0",
    description="A Discord.py‑compatible Python library for building bots on the Revolt chat platform.",
    author="revoltcord.py contributors",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "aiohttp>=3.8.0",
        "websockets>=10.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 2 - Pre-Alpha",
        "Topic :: Software Development :: Libraries",
        "Topic :: Internet",
    ],
)
