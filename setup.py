from pathlib import Path
from setuptools import find_packages, setup


setup(
    author="Eduardo Cuducos",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Utilities",
    ],
    description="Python wrapper for Central Bank of Brazil's Calculadora do Cidadão",
    install_requires=["beautifulsoup4>=4.8.2", "requests>=2.22.0",],
    keywords="Brazil, Calculadora do Cidadão",
    license="GPLv3",
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    name="calculadora-do-cidadao",
    packages=find_packages(),
    py_modules=["calculadora_do_cidadao"],
    url="https://github.com/cuducos/calculadora-do-cidadao",
    version="0.0.1",
    zip_safe=False,
)
