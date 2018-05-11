import random

import matplotlib.pyplot as plt
import seaborn as sb

plt.figure(figsize=(3, 3))
data = random.choices(population=list(range(0,10)),k=30)
sb.swarmplot(x=data, orient='v')
plt.savefig('McCreath_Benjamin_BME263_Assignment_Week4.png', dpi=600)
