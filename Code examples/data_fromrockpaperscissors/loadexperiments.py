#this will load the pickle file from the same spot
import pickle
import numpy as np
import matplotlib.pyplot as plt

# Load the list of NumPy arrays from the file
big_data_list = []
for i in ['01','02','03','04','05','06','07','08','09','10']:
    exp_filename = 'populations_experiment-' + str(i) + '.pkl'
    with open(exp_filename, 'rb') as filename:
        loaded_array_list = pickle.load(filename)
        big_data_list.append(np.array(loaded_array_list)[:5000,:])

# Define a moving average filter function
def moving_average(data, window_size=250):
    return np.convolve(data, np.ones(window_size)/window_size, mode='valid')

# Create a 5x2 grid of plots
fig, axs = plt.subplots(5, 2, figsize=(15, 25))

# Plot data on each subplot
for idx, sim in enumerate(big_data_list[:10]):
    row = idx // 2
    col = idx % 2
    smoothed_sim = np.apply_along_axis(moving_average, 0, sim)  # Apply smoothing filter
    axs[row, col].plot(smoothed_sim)
    axs[row, col].set_ylabel('Pop.')

# Adjust layout
plt.tight_layout()

# Display the figure
plt.show()