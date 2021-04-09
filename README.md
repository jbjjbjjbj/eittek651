# eittek651
Yo hvordan sker det

## Quick Start

```
$ python -m antenna_diversity
```

## Run Tests

```
$ python test.py
```

## Check Types

```
$ mypy antenna_diversity/
```

## Misc

Remember to write things that should be exposed to the user in the relevant `__init__.py` file.
Functions are in this sense "more private" than methods of an object which is exposed.
This extra layer of encapsulation is there since we want to test pure functions with docstrings.
