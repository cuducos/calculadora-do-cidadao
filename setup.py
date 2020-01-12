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
    install_requires=["aiohttp>=3.6.2", "beautifulsoup4>=4.8.0", "requests>=2.22.0"],
    keywords="Brazil, Calculadora do Cidadão",
    license="GPLv3",
    long_description=Path("README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    name="calculadora-do-cidadao",
    packages=find_packages(),
    py_modules=["calculadora_do_cidadao"],
    setup_requires=["pytest-runner"],
    tests_require=[
        "asynctest",
        "pytest",
        "pytest-asyncio",
        "pytest-black",
        "pytest-cov",
    ],
    url="https://github.com/cuducos/calculadora-do-cidadao",
    version="0.0.1",
    zip_safe=False,
)
