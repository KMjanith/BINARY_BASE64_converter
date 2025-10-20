"""
Setup script for Universal Format Converter

This allows the package to be installed as a proper Python package:
    pip install -e .        # Editable install for development
    pip install .           # Regular install
"""

from setuptools import setup, find_packages
import os

# Read the README file for long description
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "Universal Format Converter - Educational Python Project"

# Read requirements from requirements.txt
def read_requirements():
    req_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    requirements = []
    if os.path.exists(req_path):
        with open(req_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # Skip comments and empty lines
                if line and not line.startswith('#'):
                    requirements.append(line)
    return requirements

setup(
    name="universal-format-converter",
    version="1.0.0",
    author="Kavindu Janith",
    author_email="",
    description="Educational universal format converter with web GUI",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/universal-format-converter",
    
    # Package discovery
    packages=find_packages(),
    include_package_data=True,
    
    # Dependencies
    install_requires=read_requirements(),
    
    # Entry points for CLI
    entry_points={
        'console_scripts': [
            'convert=src.cli.main:main',
            'converter-web=src.web.app:main',
        ],
    },
    
    # Python version requirement
    python_requires=">=3.8",
    
    # Classification
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Multimedia :: Graphics :: Graphics Conversion",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    
    # Additional metadata
    keywords="converter, format, binary, base64, educational",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/universal-format-converter/issues",
        "Source": "https://github.com/yourusername/universal-format-converter",
        "Documentation": "https://universal-format-converter.readthedocs.io/",
    },
)