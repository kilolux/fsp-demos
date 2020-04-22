# EMAHelperFunctions.py

#################################################################

## Libraries

import matplotlib.pyplot as plt
import numpy as np


################################################################

## Exponential Moving Average (EMA) Functions

# Calculate the alpha value for a desired period.
def calculateAlpha(ema_period):
    alpha = 2.0 / (ema_period + 1)
    return alpha


# Returns the denominator
def getDenominator(number_of_terms):
    # bottom = 1 + (1-a) + (1-a)^2 + (1-a)^3 + ...
    a = calculateAlpha(number_of_terms)
    i = 0
    total = 0
    while i < number_of_terms:
        term = (1-a)**i
        total = total + term
        i = i + 1
    return total


# Returns the numerator
def getNumerator(price_data, price_data_index, number_of_terms):
    # top = p1 + (1-a)*p2 + (1-a)^2*p3 + (1-a)^3*p4 + ...
    a = calculateAlpha(number_of_terms)
    i = 0
    total = 0
    while i < number_of_terms:
        price = price_data[price_data_index - i]
        cof = (1-a)**i
        term = price * cof
        total = total + term
        i = i + 1
    return total


# Returns a single Exponential Moving Average value.
def getEMA(price_data, price_data_index, number_of_terms):
    if (number_of_terms - price_data_index) > 1:
        # There are too many terms for the given index.
        return 0
    else:
        top = getNumerator(price_data, price_data_index, number_of_terms)
        bottom = getDenominator(number_of_terms)
        EMA = np.array([top / bottom])
        return EMA

    
# Returns a list of all EMA values.
def getEMAdataset(price_data, number_of_terms):
    ema_data = np.zeros(np.size(price_data))
    i = 0
    while i < np.size(price_data):
        datum = getEMA(price_data, i, number_of_terms)
        ema_data[i] = datum
        i = i + 1
    return ema_data



####################################################################

## Plotting Function

# Plots 3 lines: raw data, EMA(period_1), EMA(period_2)
def calculateAndPlotEMA(data, ema_period_1, ema_period_2, plot_after_long_period):
    ema_1 = getEMAdataset(data, ema_period_1)
    ema_2 = getEMAdataset(data, ema_period_2)
    x = np.arange(len(data))
    plt.plot(x, data)
    plt.plot(x, ema_1)
    plt.plot(x, ema_2)
    ema_legend_text_1 = "EMA(" + str(ema_period_1) + ")"
    ema_legend_text_2 = "EMA(" + str(ema_period_2) + ")"
    plt.legend(['Value', ema_legend_text_1, ema_legend_text_2])
    plt.title("Exponential Moving Averages")
    plt.grid(b=True, which='major', color='gray', linestyle=':')
    if plot_after_long_period:
        plt.xlim(left=ema_period_2+1)
        plt.ylim(bottom=min(data)-5)
    plt.show()
    
########################################################################

## Sine Wave Function

# Generates a sine wave.
def generateSineWave(period, amplitude, sigma, end):
    # Equations
    alpha = amplitude / 2.0
    beta = 2.0 * np.pi / period
    frequency = 1.0 / period
    x = np.arange(end + 1)
    
    # Formula
    y = alpha * np.sin(beta * x) + sigma
    return y

################################################################

# MACD Function

# Given the signal data and the 3 periods, calculate all of the indicators.
def getMACD(signal_data, ema_short_period, ema_long_period, macd_signal_period):
    
    # Create timeline
    x = np.arange(len(signal_data))
    
    # Calculate Exponential Moving Averages
    ema_short_data = getEMAdataset(signal_data, ema_short_period)
    ema_long_data  = getEMAdataset(signal_data, ema_long_period)
    
    # Calculate MACD
    MACD = ema_short_data - ema_long_data
    # for all initial values leading to the EMA_long_period, make zero.
    # This cleans up the initial "spin-up" error.
    MACD[0:ema_long_period - 1] = 0
    
    # Calculate EMA of the MACD
    MACD_signal = getEMAdataset(MACD, macd_signal_period)
    
    # Calculate MACD difference, which is plotted as a bar chart.
    MACD_bars = MACD - MACD_signal
    
    # Return Everything
    return x, ema_short_data, ema_long_data, MACD, MACD_signal, MACD_bars


# Plotting Function

def plotMACD(x, MACD_data, MACD_signal_data, macd_signal_period, MACD_hist, plot_x_start, plot_x_end):
    plt.plot(x, MACD_data, color='blue')
    plt.plot(x, MACD_signal_data, color='red')
    plt.bar(x, MACD_hist, color='black')
    #plt.axhline(y=0.0, color='k', linestyle='--')
    legend_text_1 = "MACD"   
    legend_text_2 = "MACD_signal(" + str(macd_signal_period) + ")"
    legend_text_3 = "MACD_hist"
    plt.legend([legend_text_1, legend_text_2, legend_text_3])
    plt.title("MACD and MACD_signal")
    plt.grid(b=True, which='major', color='gray', linestyle=':')
    plt.xlim((plot_x_start, plot_x_end))
    plt.show()