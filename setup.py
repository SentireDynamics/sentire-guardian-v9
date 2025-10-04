"""
Setup - Configuration du Package Guardian V9

Installation du Vaisseau Guardian V9 comme package Python.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Lire le README pour la description longue
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

setup(
    name="sentire-guardian-v9",
    version="9.0.0",
    author="Sentire Dynamics - Collège des Architectes Souverains",
    author_email="contact@sentiredynamics.com",
    description="Vaisseau Souverain Guardian V9 - Architecture TPD v1.2, Résilience Digitale",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SentireDynamics/sentire-guardian-v9",
    project_urls={
        "Bug Tracker": "https://github.com/SentireDynamics/sentire-guardian-v9/issues",
        "Documentation": "https://github.com/SentireDynamics/sentire-guardian-v9/tree/main/docs",
        "Source Code": "https://github.com/SentireDynamics/sentire-guardian-v9",
    },
    packages=find_packages(exclude=["tests", "tests.*", "csrc", "docs"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: System :: Monitoring",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: C",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=[
        "PyQt6>=6.6.0",
        "pydantic>=2.5.0",
        "numpy>=1.24.0",
        "scikit-learn>=1.3.0",
        "requests>=2.31.0",
        "cffi>=1.16.0",
        "python-dotenv>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.7.0",
        ],
        "drl": [
            "torch>=2.1.0",
            "torchvision>=0.16.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "guardian-v9=guardian.main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "guardian": ["ui/qss/*.qss"],
    },
    zip_safe=False,
)
