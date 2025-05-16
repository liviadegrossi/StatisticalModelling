import matplotlib.pyplot as plt
import numpy as np
import math
import pandas as pd
import geopandas as gpd
import rasterio
import rasterio.plot as rplt 
from sklearn.linear_model import LinearRegression 

# Exercise: Estimating variance-covariance matrix of temperature and precipitation
# temperature = np.array([86, 81, 83, 89, 80, 74, 64])
# precipitation = np.array([3.4, 1.8, 3.5, 3.6, 3.7, 1.5, 0.2])

# # Step 1: Observe the relationship between temperature and precipitation
# fig, ax = plt.subplots()
# ax.plot(temperature, precipitation, 'o', color='blue', label='Data Points')
# ax.set_xlabel('Temperature (°F)')
# ax.set_ylabel('Precipitation (mm)')

# # Step 2: Fit a linear regression (b1 = slope, b0 = intercept)
# b1, b0 = np.polyfit(temperature, precipitation, deg=1)
# ax.plot(temperature, b0 + b1 * temperature, color='red', label='Fitted Line')
# # plt.show()

# # Step 3: Centering the variables
# temperature_centered = temperature - np.mean(temperature)
# precipitation_centered = precipitation - np.mean(precipitation)

# # Step 4: Create the data matrix
# dataMatrix = np.array([temperature_centered, precipitation_centered])

# # Step 5: Calculate the variance-covariance matrix
# covariance_matrix = np.cov(dataMatrix)
# print("Variance-Covariance Matrix:", covariance_matrix)

# # Step 6: Calculate the correlation coefficient
# correlation_coefficient = covariance_matrix[0, 1] / (math.sqrt(covariance_matrix[0, 0]) * math.sqrt(covariance_matrix[1, 1]))
# correlation_coefficient_for = np.corrcoef(temperature, precipitation)[0, 1] # Using numpy method                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       for verification
# print("Correlation Coefficient:", correlation_coefficient)
# print("Correlation Coefficient (numpy):", correlation_coefficient_for)

# Exercise: Analyzing the impact of elevation on rainfall in Switzerland

# Step 1: Load the rinfall data
dataFrame = pd.read_table('./Data/sic_obs.dat', delimiter=',', header=0)
print(dataFrame.head())

geoDataFrame = gpd.GeoDataFrame(dataFrame, geometry=gpd.points_from_xy(dataFrame.x_coor, dataFrame.y_coor), crs='EPSG:3857')
print(geoDataFrame.head())

# Step 2: Read the boarders of the study area
shpBorders = gpd.read_file('./Data/borders.shp')

# Step 3: Read the elevation data (DEM)
DEM = rasterio.open('./Data/DEM.grd')
DEM_data = DEM.read(1) # read the single band

# Step 4: Show all the layers combined
fig, ax = plt.subplots()

ax = rasterio.plot.show(DEM, ax=ax)
shpBorders.plot(ax=ax, color='yellow')
geoDataFrame.plot(ax=ax, color='red', markersize=5)
plt.show()

# Step 5: Retrieve the number of bands in the DEM
bands = DEM.count
print('Bands: ', bands)

# Step 6: Create an additional column for the geoDataFrame to store DEM values
geoDataFrame['dem'] = 0

# Step 7: Extrat the DEM for each geoDataFrame point
for index, row in geoDataFrame.iterrows():
    longitude = row['geometry'].x   
    latitude = row['geometry'].y

    # Cel's row and column indexes in the raster data (DEM)
    rowIndex, colIndex = DEM.index(longitude, latitude)
    geoDataFrame.loc[index, 'dem'] = DEM_data[rowIndex, colIndex]

print(geoDataFrame.head())

# Step 8: Estimating the correlation between rainfall and DEM
corrPearson = geoDataFrame['rain_mm'].corr(geoDataFrame['dem'], method='pearson')
corrSpearman = geoDataFrame['rain_mm'].corr(geoDataFrame['dem'], method='spearman')
print('Pearson correlation coefficient: ', corrPearson)
print('Spearman correlation coefficient: ', corrSpearman)

# Step 9: Visualizing the relationship between rainfall and DEM
plt.plot(geoDataFrame['dem'], geoDataFrame['rain_mm'], 'o', color='blue')
plt.show()

# Step 10: Fit a simple linear regression model
simpleLR = LinearRegression().fit(geoDataFrame[['dem']], geoDataFrame['rain_mm'])
# print('Linear regression model: ', simpleLR)

# Step 11: Data transformation using the centering technique
geoDataFrame['rain_center'] = 0
# print(geoDataFrame['rain_mm'])
print('Mean: ', np.mean(geoDataFrame[['rain_mm']]))
print('Mean: ', np.mean(geoDataFrame['rain_mm']))

geoDataFrame['rain_center'] = geoDataFrame['rain_mm'].apply(lambda x: x - np.mean(geoDataFrame['rain_mm']))
print(geoDataFrame.head())

# Step 12: Visualizing the relationship between rainfall and DEM after centering
# plt.plot(geoDataFrame['dem'], geoDataFrame['rain_center'], 'o', color='blue')
# plt.show()