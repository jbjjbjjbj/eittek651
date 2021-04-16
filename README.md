# eittek651
Yo hvordan sker det

## Install Libraries

```
pip3 install -r requirements.txt
```

If the pip3 utility is not in your path but `python3` is, use the following.

```
python3 -m pip install -r requirements.txt
```

## Quick Start

```
$ python3 -m antenna_diversity
```

## Run Tests

```
$ python3 test.py
```

## Check Types

```
$ mypy antenna_diversity/
```

## Misc

Remember to write things that should be exposed to the user in the relevant `__init__.py` file.
Functions are in this sense "more private" than methods of an object which is exposed.
This extra layer of encapsulation is there since we want to test pure functions with docstrings.

## Running ModulationTest

This is done from a python shell.

```python
import antenna_diversity.modulation as mod
mod.ModulationTest.plot(mod.PAM(4), (-10, 20), 10)
```
