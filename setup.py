from pathlib import Path

from setuptools import find_packages, setup

setup(
    author="Eduardo Cuducos",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Utilities",
    ],
    description="Tool for Brazilian Reais monetary adjustment/correction",
    install_requires=["requests>=2.22.0", "rows[html,xls]>=0.4.1"],
    keywords="Brazil, Brazilian reais, monetary adjusment, monetary correction, IPCA",
    license="GPLv3",
    long_description=Path("README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    name="calculadora-do-cidadao",
    packages=find_packages(),
    py_modules=["calculadora_do_cidadao"],
    url="https://github.com/cuducos/calculadora-do-cidadao",
    version="0.0.4",
    zip_safe=False,
)
