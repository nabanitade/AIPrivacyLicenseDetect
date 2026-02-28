from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ai-privacy-license-detector",
    version="1.0.0",
    author="AI Privacy License Team",
    author_email="contact@aiprivacylicense.com",
    description="Detect and respect AI Privacy Licenses when crawling or processing data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nabanitade/aiprivacylicenseSDK",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.25.0",
        "beautifulsoup4>=4.9.0",
        "urllib3>=1.26.0",
        "pyyaml>=5.4.0",
        "dataclasses>=0.8; python_version<\"3.7\"",
        "typing-extensions>=3.7.0; python_version<\"3.8\""
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov",
            "black",
            "isort",
            "mypy",
            "pre-commit"
        ],
        "docs": [
            "sphinx",
            "sphinx-rtd-theme",
            "myst-parser"
        ],
        "integration": [
            "scrapy>=2.0",
            "langchain>=0.0.200",
            "mlflow>=2.0",
            "openai>=1.0"
        ]
    },
    entry_points={
        "console_scripts": [
            "ai-license=ai_privacy_license_detector.cli:main",
        ],
    },
    include_package_data=True,
)
