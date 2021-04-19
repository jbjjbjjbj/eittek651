# This pretends as if it were the antenna_diversity module
import os
from pathlib import Path
filepath = os.path.realpath(__file__)
os.chdir(Path(filepath).parent)
import antenna_diversity
