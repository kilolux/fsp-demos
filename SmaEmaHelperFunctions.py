# SmaEmaHelperFunctions.py

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

################################################################

# SMA Functions

# Calculates the average given a list of numbers.
def getAvg(data):
    total = 0
    i = 0
    while i < len(data):
        total = total + data[i]
        i = i + 1
    # Catch divide by zero errors.
    if i == 0: 
        return 0
    else:
        return total / i

    
# Produces a subset list given a list of numbers, the final 
#desired index, and the desired subset length.
def getMovingList(data, index, length):
    listEnd = index + 1
    listStart = index - length + 1
    result = data[listStart:listEnd]
    # Note that when index - length < -1, then the result will be [] (empty)
    return result


# Calculates a single average.
def getSingleSMA(data, index, sma_period):
    movingList = getMovingList(data, index, sma_period)
    average = getAvg(movingList)
    return average


# Calculates the entire list of averages.
def getSMAlist(data, sma_period):
    smaList = []
    i = 0
    while i < len(data):
        value = getSingleSMA(data, i, sma_period)
        smaList.append(value)
        i = i + 1
    return smaList

################################################################

# Plotting Functions

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
