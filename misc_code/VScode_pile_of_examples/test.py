import numpy as np

import matplotlib.pyplot as plt

# Define the x values
x = np.linspace(0, 1, 400)

# Define the y values as sin(2 * pi * x)
y = np.sin(2 * np.pi * x)

# Create the plot
plt.plot(x, y)

# Add title and labels
plt.title('Plot of sin(2πx) on the unit interval [0, 1]')
plt.xlabel('x')
plt.ylabel('sin(2πx)')

# Show the plot
plt.grid(True)
plt.show()