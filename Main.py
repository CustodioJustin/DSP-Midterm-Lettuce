import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import periodogram

class Periodogram:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = pd.read_excel(self.file_path)

    def process_periodogram_data(self, column_name):
        time_series_data = [float(row[column_name]) for index, row in self.data.iterrows()]
        frequencies, power_spectrum = periodogram(time_series_data)

        nonzero_freq = [freq for freq, power in zip(frequencies, power_spectrum) if freq != 0]
        nonzero_power = [power for freq, power in zip(frequencies, power_spectrum) if freq != 0]

        return nonzero_freq, nonzero_power

    def compute_periodogram(self, column_name):
        nonzero_freq, nonzero_power = self.process_periodogram_data(column_name)
        return nonzero_freq, nonzero_power

    def compute_smooth_periodogram(self, column_name, filter_size=10):
        nonzero_freq, nonzero_power = self.process_periodogram_data(column_name)
        smoothed_power_spectrum = np.convolve(nonzero_power, np.ones(filter_size) / filter_size, mode='same')
        return nonzero_freq, smoothed_power_spectrum

    # Removes any data that is 0
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

DataSheet = Periodogram('DSP Data Collection.xlsx')

frequencies, power_spectrum = DataSheet.compute_periodogram("Temperature (Celsius)")
sm_frequencies, sm_power_spectrum = DataSheet.compute_smooth_periodogram("Temperature (Celsius)")
DataSheet.plot_periodogram(frequencies, power_spectrum, "Temperature")
DataSheet.plot_periodogram(sm_frequencies, sm_power_spectrum, "Temperature_Smoothen")

frequencies, power_spectrum = DataSheet.compute_periodogram("Humidity")
sm_frequencies, sm_power_spectrum = DataSheet.compute_smooth_periodogram("Humidity")
DataSheet.plot_periodogram(frequencies, power_spectrum, "Humidity")
DataSheet.plot_periodogram(sm_frequencies, sm_power_spectrum, "Humidity_Smoothen")
