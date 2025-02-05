from setuptools import setup, find_packages

setup(
    name="agile-stories",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.104.0",
        "uvicorn>=0.24.0",
        "pydantic>=2.4.2",
        "python-dotenv>=1.0.0",
        "openai>=1.3.0",
        "redis>=5.0.1",
        "boto3>=1.29.0",
        "pyyaml>=6.0.1",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "black>=23.11.0",
            "isort>=5.12.0",
            "mypy>=1.7.0",
        ]
    },
)