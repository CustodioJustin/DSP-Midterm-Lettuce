import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import periodogram

class Periodogram:
    def __init__(self, file_path):
        """
        Initializes the Periodogram class, setting the file path for data retrieval.
        """
        self.file_path = file_path
        self.data = pd.read_excel(self.file_path)

    def process_periodogram_data(self, column_name):
        """
        Processes the data for a specified column by computing the periodogram.
        Edit: Adds a method to skip rows where data is empty.  This must be added else
        graphing daily and weekly isn't correct
        """
        time_series_data = [float(row[column_name]) for index, row in self.data.iterrows() if not pd.isnull(row[column_name])]
        frequencies, power_spectrum = periodogram(time_series_data)

        nonzero_freq = [freq for freq, power in zip(frequencies, power_spectrum) if freq != 0]
        nonzero_power = [power for freq, power in zip(frequencies, power_spectrum) if freq != 0]

        return nonzero_freq, nonzero_power

    def compute_periodogram(self, column_name):
        """
        Computes the periodogram for the specified column, utilizing processed data.
        """
        nonzero_freq, nonzero_power = self.process_periodogram_data(column_name)
        return nonzero_freq, nonzero_power

    def compute_smooth_periodogram(self, column_name, filter_size=10):
        """
        Computes a smoothed periodogram by applying low pass filtering to the data.
        """
        nonzero_freq, nonzero_power = self.process_periodogram_data(column_name)
        smoothed_power_spectrum = np.convolve(nonzero_power, np.ones(filter_size) / filter_size, mode='same')
        return nonzero_freq, smoothed_power_spectrum

    def plot_periodogram(self, frequencies, power_spectrum, column_name):
        """
        Plots the periodogram graph based on computed frequencies and power spectrum.
        Saves the graph as an image file and displays it.
        """
        plt.figure(figsize=(8, 4))
        plt.semilogy(frequencies, power_spectrum)
        plt.title(f'{column_name} - Periodogram')
        file_name = f'{column_name}_Periodogram.png'

        plt.xlabel('Frequency')
        plt.ylabel('Power Spectral Density')
        plt.grid(True)

        directory = 'Periodograms'
        if not os.path.exists(directory):
            os.makedirs(directory)

        file_path = os.path.join(directory, file_name)
        plt.savefig(file_path, format='png', dpi=300)
        plt.show()

DataSheet = Periodogram('DSP Data Collection.xlsx')

# Displaying non-smooth periodogram for Temperature
frequencies, power_spectrum = DataSheet.compute_periodogram("Temperature (Celsius)")
DataSheet.plot_periodogram(frequencies, power_spectrum, "Temperature - 15m Interval")

# Displaying non-smooth periodogram for Humidity
frequencies, power_spectrum = DataSheet.compute_periodogram("Humidity")
DataSheet.plot_periodogram(frequencies, power_spectrum, "Humidity - 15m Interval")

# Displaying non-smooth periodogram for Temperature Daily
frequencies, power_spectrum = DataSheet.compute_periodogram("Temperature - Daily")
DataSheet.plot_periodogram(frequencies, power_spectrum, "Temperature - Daily")

# Displaying non-smooth periodogram for Humidity Daily
frequencies, power_spectrum = DataSheet.compute_periodogram("Humidity - Daily")
DataSheet.plot_periodogram(frequencies, power_spectrum, "Humidity - Daily")


# Displaying smooth periodogram for Temperature
frequencies, power_spectrum = DataSheet.compute_smooth_periodogram("Temperature (Celsius)")
DataSheet.plot_periodogram(frequencies, power_spectrum, "Temperature - 15m Interval (Low Pass Filter)")

# Displaying smooth periodogram for Humidity
frequencies, power_spectrum = DataSheet.compute_smooth_periodogram("Humidity")
DataSheet.plot_periodogram(frequencies, power_spectrum, "Humidity - 15m Interval (Low Pass Filter)")

