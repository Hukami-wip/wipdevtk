from setuptools import find_packages, setup

setup(
    name="wipdevtk",
    version="0.1.0",
    description="Worlds In Process Development Toolkit",
    author="Your Name",
    author_email="email@example.com",
    packages=find_packages(),
    python_requires=">=3.12",
    install_requires=[
        "sqlalchemy>=2.0.0",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
