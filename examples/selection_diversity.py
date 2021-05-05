import ad_path
import numpy as np
from antenna_diversity import diversity_technique

ad_path.nop()


#
# contruct a channel h
h = np.array([0.8, 1.2, 1])
# create signal
x = np.matrix('1 2 3 ; 4 5 6 ; 7 8 9')
print('x:', x)
# selection from h example

y, index = diversity_technique.selection_from_h(x, h)

# selection from power example
y1, index1 = diversity_technique.selection_from_power(x, h)


print("y:", y)
print("index:", index)
print("h:", h[index])

print("y1:", y)
print("index1", index1)
