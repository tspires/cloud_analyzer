from setuptools import setup, find_packages

setup(
    name="cloud-analyzer-cli",
    version="0.1.0",
    description="Multi-cloud cost optimization analyzer - CLI",
    author="Cloud Analyzer Team",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.11",
    install_requires=[
        "click>=8.1.7",
        "rich>=13.7.0",
        "tabulate>=0.9.0",
        "pyyaml>=6.0",
        "python-dateutil>=2.8.2",
    ],
    entry_points={
        "console_scripts": [
            "cloud-analyzer=main:cli",
        ],
    },
)