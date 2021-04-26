import ad_path
import numpy as np
from antenna_diversity import diversity

ad_path.nop()

# contruct a channel h
h = np.array([0.8, 1.2, 1])
# create signal
x = np.matrix('1 2 3 ; 4 5 6 ; 7 8 9')
print('x:', x)

y, index = diversity.Selection.selection(x, h)

print("y:", y)
print("index:", index)
print("h:", h[index])
