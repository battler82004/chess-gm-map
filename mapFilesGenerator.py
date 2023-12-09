# Map Files Generator
# James Taddei
# 12/9/2023

def main():
    """
    Creates a GEOJSON file for each year (1950-2023) storing a world map.
    """
    for year in range(1950, 2024):
        generateMapForYear(year)

def generateMapForYear(year) -> None:
    """
    Creates a map file (GEOJSON) for the world at the end of a given year.
    """
    # Variable declarations
    mapFile = "countryReferenceMap.geojson"
    writingFile = f"mappingData\\{year}.geojson"

    inFile = open(mapFile, "r")
    outFile = open(writingFile, "w")

    if (year >= 1959): # accounts for the first lines missing when the first country is not included
        outFile.write('{\n\t"type": "FeatureCollection",\n\t"features": [\n')

    while (True): # keep looping between countries
        # Variables
        reloop = True
        shouldAdd = True
        line = ""
        currText = ""

        # Keep looping through the file until the end of a specific country
        while (line != "\t\t},\n"):
            line = inFile.readline()
            currText += line

            if (line.startswith('\t\t\t\t"gwcode": ')): # if is distinct country
                gwCode = int((line.split(" ")[1]).split(",")[0])
                if ((gwCode != 9401) and (gwCode <= 989)): # if is a valid country with GM data
                    currText += getGmData(gwCode, year) # add GM data
                else: # final country (never included)
                    outFile.write("]\n}")
                    reloop = False
                    break

            if (line.startswith('\t\t\t\t"gwsyear": ')): # determines startYear
                startYear = int((line.split(" ")[1]).split(",")[0])
                print(f"startYear - {startYear}")
            if (line.startswith('\t\t\t\t"gweyear": ')): # determines endYear
                endYear = int((line.split(" ")[1]).split(",")[0])
                print(f"endYear - {endYear}")
                # Only add if startYear <= year < endYear because map is based on
                # end of year (12/31/year)
                if ((startYear > year) or (year >= endYear)):
                    shouldAdd = False

        if not(reloop): # If at the end of the file
            break

        if (shouldAdd): # If the country existed during the given year
            outFile.write(currText)

    inFile.close()
    outFile.close()

    # Remove comma because last item is not included
    with open(writingFile, "r") as outFile: # Reads data
        lines = outFile.readlines()
    with open(writingFile, "w") as outFile: # Removes comma and rewrites data
        lines[-3] = "\t\t}\n"
        outFile.writelines(lines)

def getGmData(gwCode, year) -> str:
    """
    Generates and returns the JSON line which holds the numOfGms attribute.
    """
    dataPath = f"thematicData\\{year}.txt"
    with open(dataPath, "r") as file:
        for _ in range(gwCode + 3):
            line = file.readline()

    numOfGms = int(line.split(",")[1])
    return f'\t\t\t\t"numOfGms": {numOfGms}, \n'

main()