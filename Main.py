import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import periodogram

class Periodogram:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = pd.read_excel(self.file_path)

    # Process a specified row of data from the excel sheet. It also filters out
    # any data that is exactly 0.
    def process_periodogram_data(self, column_name):
        time_series_data = [float(row[column_name]) for index, row in self.data.iterrows()]
        frequencies, power_spectrum = periodogram(time_series_data)

        nonzero_freq = [freq for freq, power in zip(frequencies, power_spectrum) if freq != 0]
        nonzero_power = [power for freq, power in zip(frequencies, power_spectrum) if freq != 0]

        return nonzero_freq, nonzero_power

    # Computes the data into a periodogram (refer to the last method).
    # This is done to separate on computing the original data and computing and smoothing of data
    def compute_periodogram(self, column_name):
        nonzero_freq, nonzero_power = self.process_periodogram_data(column_name)
        return nonzero_freq, nonzero_power

    # Like the previous method, this simply process for periodogram but also smoothen the results by
    # applying low pass filtering.
    def compute_smooth_periodogram(self, column_name, filter_size=10):
        nonzero_freq, nonzero_power = self.process_periodogram_data(column_name)
        smoothed_power_spectrum = np.convolve(nonzero_power, np.ones(filter_size) / filter_size, mode='same')
        return nonzero_freq, smoothed_power_spectrum

    # Plots the data on a graph and export the graph in a jpg image
    def plot_periodogram(self, frequencies, power_spectrum, column_name):

        plt.figure(figsize=(8, 4))
        plt.semilogy(frequencies, power_spectrum)
        plt.title('Periodogram')
        plt.xlabel('Frequency')
        plt.ylabel('Power Spectral Density')
        plt.grid(True)

        directory = 'Periodograms'
        if not os.path.exists(directory):
            os.makedirs(directory)

        file_path = os.path.join(directory, f'{column_name}_periodogram.png')
        plt.savefig(file_path, format='jpg')
        plt.show()

# Specify the excel sheet
DataSheet = Periodogram('DSP Data Collection.xlsx')

# Compute and plot a periodogram for temperature
frequencies, power_spectrum = DataSheet.compute_periodogram("Temperature (Celsius)")
sm_frequencies, sm_power_spectrum = DataSheet.compute_smooth_periodogram("Temperature (Celsius)")
DataSheet.plot_periodogram(frequencies, power_spectrum, "Temperature")
DataSheet.plot_periodogram(sm_frequencies, sm_power_spectrum, "Temperature_Smoothen")

# Compute and plot a periodogram for humidity
frequencies, power_spectrum = DataSheet.compute_periodogram("Humidity")
sm_frequencies, sm_power_spectrum = DataSheet.compute_smooth_periodogram("Humidity")
DataSheet.plot_periodogram(frequencies, power_spectrum, "Humidity")
DataSheet.plot_periodogram(sm_frequencies, sm_power_spectrum, "Humidity_Smoothen")
