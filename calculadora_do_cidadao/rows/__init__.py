"""
This module conatins only files form a third-party package that cannot be
installed via `pip`:
https://github.com/cuducos/calculadora-do-cidadao/issues/51

We kept the copy files mostly as close as possible to what they were in their
source at the commit fcf226fdc779687df81ee586a31a8acf3f38f715, just clenaing up
and adapting to what is needed in order to work with this package. As as soon
as Rows have a new release we can remove this module and install from `pip`:

- reverting the commit that has created this file
- updating Rows version in pyproject.toml
"""
