import matplotlib.patches as mplpatches
import matplotlib.pyplot as plt

plt.style.use('BME163.mplstyle')
fig_width = 5
fig_height = 2
plt.figure(figsize=(fig_width, fig_height))
panel_width = 1.5 / fig_width
panel_height = 1.5 / fig_height
panel1 = plt.axes([0.1, 0.1, panel_width, panel_height])
panel2 = plt.axes([0.6, 0.1, panel_width, panel_height])
panel1.plot([5, 0.75], [0.75, 0.25], \
            marker='o', \
            linewidth=0, \
            markeredgecolor='black', \
            markerfacecolor='red', \
            markeredgewidth=0, \
            markersize=10)
rectangle = mplpatches.Rectangle((0.25, 0.25), 0.5, 0.5, \
                                 facecolor=(0, 0.5, 1), \
                                 edgecolor='black', \
                                 linewidth=0)
panel2.add_patch(rectangle)
plt.savefig('Vollmers_Lecture1.png', dpi=600)
