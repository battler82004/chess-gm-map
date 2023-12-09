# Chess GMs Map
# James Taddei
# 12/9/2023

# Resolves error of the program having no path
import os
os.environ['PROJ_LIB'] = "C:\\Users\\battl\\miniconda3\\envs\\termproject\\Library\\share\\proj"
os.environ['GDAL_DATA'] = "C:\\Users\\battl\\miniconda3\\envs\\termproject\\Library\\share"

# Imports
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import shapely
import fiona

def main():
     """
     Go through each year (1950-2023) and calls for a
     map to be generated and saved.
     """
     endYear = 2023
     shouldSave = True
     for year in range(1950, endYear + 1):
          mapYearSave(year, shouldSave)

def mapYearWithChart(year, shouldSave) -> None:
     """
     Generates and shows/saves a map for the given year.
     """
     mapFile = f"mappingData\\{year}.geojson"
     with open(mapFile) as referenceData:
          countries = gpd.read_file(referenceData)

          # Creates the subplots
          fig, (ax1, ax2) = plt.subplots(ncols=2, width_ratios=[3, 1])
          fig.subplots_adjust(bottom=0.2)

          # Plot map
          countries.plot(ax=ax1, column="numOfGms", cmap="OrRd", legend=True, edgecolor="black")
          ax1.set_title(f"Number of Chess GMs by Country in {year}")
          ax1.set_xlabel(f"Total number of GMs: {getNumOfGms(year)}")
          ax1.axis("off")

          # Plot top 10 countries graph
          top10Countries, top10Nums = getTop10Countries(year)
          ax2.bar(top10Countries, top10Nums, color ='maroon', width = 0.4)
          ax2.set_title("Top 10 Countries with Most GMs")
          ax2.set_xticklabels(ax2.get_xticklabels(), rotation=90)

          if (shouldSave): # saves the map to the program folder
               pass
          else: # show the map to the user
               plt.show()

def mapYearSave(year, shouldSave) -> None:
     """
     Generates and shows/saves a map for the given year.
     """
     mapFile = f"mappingData\\{year}.geojson"
     with open(mapFile) as referenceData:
          countries = gpd.read_file(referenceData)

          # Plots the map and manipulates the settings
          countries.plot(column="numOfGms", cmap="Reds", legend=True, edgecolor="black", legend_kwds={'shrink': 0.7})
          plt.title(f"Number of Chess GMs by Country in {year}")
          plt.xlabel(f"Total number of GMs: {getNumOfGms(year)}")
          plt.xticks([]) # removes x-axis (but keeps label)
          plt.yticks([])

          plt.tight_layout()

          if (shouldSave): # saves the map to the program folder
               plt.savefig(f"generatedMaps\\{year}.png")
          else: # show the map to the user
               plt.show()

def getNumOfGms(year) -> str:
     """
     Returns the total number of alive GMs for the given year.
     """
     dataPath = f"thematicData\\{year}.txt"
     with open(dataPath, "r") as file:
          return file.readline()
     
def getTop10Countries(year) -> list:
     """
     Returns a list of the top 10 countries by number of GMs on
     the given year. The list contains 2 sublists: the top 10 countries
     (as GW Codes) and the respective number of GMs.
     """
     dataPath = f"thematicData\\{year}.txt"
     with open(dataPath, "r") as file:
          for _ in range(2):
               line = file.readline()
          
     # Splits the data into a sublist for each country: [gwCode, numOfGms]
     rawData = line.split(";")
     for i in range(len(rawData)):
          rawData[i] = rawData[i].split(",")
          rawData[i][0] = rawData[i][0]
          rawData[i][1] = int(rawData[i][1])

     # Changes to the output format: [coutries, numOfGms]
     top10Data = [[], []] # [countries, numOfGms]
     for country in range(10):
          top10Data[0].append(rawData[country][0]) # copy gwCode
          top10Data[1].append(rawData[country][1]) # copy numOfGms

     convertFromGw(top10Data[0]) # converts GW codes to country names

     return top10Data

def convertFromGw(countriesAsGw) -> None:
     """
     Converts a list of 10 GW code into 10 country names
     """
     dataPath = "gwCodes.txt"
     for i in range(10):
          # Finds the line for the given country and changes the GW code
          # to the country's name
          with open(dataPath, "r") as file:
               for line in file:
                    curr = line.split(",")
                    if (curr[0] == countriesAsGw[i]):
                         countriesAsGw[i] = curr[1]

     # No return, updates list passed as reference instead

main()