from setuptools import setup, find_packages

setup(
    name="rb_eit",
    version="0.1.0",
    description="Rb double-lambda EIT atomic system model",
    author="CTO.new",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.20.0",
        "scipy>=1.7.0",
        "matplotlib>=3.3.0",
        "plotly>=5.0.0",
        "click>=8.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=3.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "fwm-sim=rb_eit.cli:cli",
        ],
    },
)
