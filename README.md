# eittek651

Software for bachalor projekt, simulating antenna diversity selection algorithms.
The folder `antenna_diversity` contains the framework for writing simulations, while `examples` contains simulations used in the report.

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

## Compare Simulated Modulation to Theoretical Modulation

This can be done from a python shell:

```python
import antenna_diversity.modulation as mod
import numpy as np
mod.Runner.plot(mod.PAM(4), np.array([-5, -10]), 10).savefig("out.png")
```

## Profile an Example

You can do this any which way you like, but here is with cProfile and snakeviz:

```
$ python -m cProfile -o hello.prof examples/hello_world.py
$ snakeviz hello.prof
```


