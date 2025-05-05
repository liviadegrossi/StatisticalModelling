import matplotlib.pyplot as plt
import numpy as np
import math

# Exercise: Estimating variance-covariance matrix of temperature and precipitation
temperature = np.array([86, 81, 83, 89, 80, 74, 64])
precipitation = np.array([3.4, 1.8, 3.5, 3.6, 3.7, 1.5, 0.2])

# Step 1: Observe the relationship between temperature and precipitation
fig, ax = plt.subplots()
ax.plot(temperature, precipitation, 'o', color='blue', label='Data Points')
ax.set_xlabel('Temperature (°F)')
ax.set_ylabel('Precipitation (mm)')

# Step 2: Fit a linear regression (b1 = slope, b0 = intercept)
b1, b0 = np.polyfit(temperature, precipitation, deg=1)
ax.plot(temperature, b0 + b1 * temperature, color='red', label='Fitted Line')
plt.show()

# Step 3: Centering the variables
temperature_centered = temperature - np.mean(temperature)
precipitation_centered = precipitation - np.mean(precipitation)

# Step 4: Create the data matrix
dataMatrix = np.array([temperature_centered, precipitation_centered])

# Step 5: Calculate the variance-covariance matrix
covariance_matrix = np.cov(dataMatrix)
print("Variance-Covariance Matrix:", covariance_matrix)

# Step 6: Calculate the correlation coefficient
correlation_coefficient = covariance_matrix[0, 1] / (math.sqrt(covariance_matrix[0, 0]) * math.sqrt(covariance_matrix[1, 1]))
correlation_coefficient_for = np.corrcoef(temperature, precipitation)[0, 1] # Using numpy method                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       for verification
print("Correlation Coefficient:", correlation_coefficient)
print("Correlation Coefficient (numpy):", correlation_coefficient_for)