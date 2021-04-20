# This pretends as if it were the antenna_diversity module
import os
import sys
from pathlib import Path

filepath = Path(os.path.realpath(__file__))
sys.path.append(str(filepath.parent.parent))
