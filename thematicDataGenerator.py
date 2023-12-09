# Thematic Data Generator
# James Taddei
# 12/9/2023

import pyexcel as p

def main():
    """
    Determines the GM data for each year and stores it in a file.
    """
    # Variable declarations
    records = p.get_sheet(file_name="chessGms.xlsx").get_array()
    countryData = [0]*990
    maxPos = 0

    # Goes through each year in the range and recalculates the number of GMs in
    # each country before tallying up the total number, determining the countries
    # with the most GMs, and creates a file holding that data.
    for year in range(1950, 2024):
        # Recalculate number of GMs by country
        removeDead(records, countryData, maxPos, year)
        updateFederations(records, countryData, maxPos, year)
        maxPos = addNewTitles(records, countryData, maxPos, year)

        # Determine extra data
        currNumOfGms = sum(countryData)
        top10Countries = determineTop10Countries(countryData)

        # Stores the year's data
        createFile(countryData, currNumOfGms, top10Countries, year)

def removeDead(records, countryData, maxPos, year) -> None:
    """
    Removes GMs who died on a given year from the tally.
    """
    # Go up through each GM in the file and removes dead GMs from
    # the tally.
    for i in range(0, maxPos):
        record = records[i]
        if (isinstance(record[0], str)):
            continue
        if (year == record[0].year):
            countryData[deathCountry(record)] -= 1

def deathCountry(record) -> int:
    """
    Returns the federation that the player was a part of
    when they died.
    """
    if (isinstance(record[5], int)): # died in 3rd federation
        return int(record[6])
    if (isinstance(record[3], int)): # died in 2nd federation
        return int(record[4])
    return int(record[2]) # died in 1st federation

def updateFederations(records, countryData, maxPos, year) -> None:
    """
    Updates the number of GMs counter for relevant countries for
    each GM that changed federations on a given year.
    """
    for i in range(0, maxPos):
        record = records[i]
        if (isinstance(record[5], int)):
            if (year == int(record[5])): # if changing to 3rd federation
                countryData[record[4]] -= 1 # remove from 2nd fed
                countryData[record[6]] += 1 # add to 3rd
        if (isinstance(record[3], int)):
            if (year == int(record[3])): # if changing to 2nd federation
                countryData[record[2]] -= 1 # remove from 1st fed
                countryData[record[4]] += 1 # add to 2nd

def addNewTitles(records, countryData, maxPos, year) -> int:
    """
    Adds GMs who received the title on a year to the counter.
    Returns the new maxPos of the program based on the year.
    """
    for i in range(maxPos, 2044):
        record = records[i]
        if (int(record[1]) > year):
            return i # this is the new maxPos, where to start/stop looking later
        countryData[record[2]] += 1

def determineTop10Countries(countryData):
    """
    Returns a list of the top 10 (increasing) countries in terms
    of number of GMs.
    """
    return sorted(range(len(countryData)), key=lambda i: countryData[i])[-10:]

def createFile(countryData, currNumOfGms, top10Countries, year):
    """
    Creates and writes to a file for the given year. It stores the
    current number of GMs, the 10 countries with the most GMs, and
    the number of GMs for each country.
    """
    fileName = f"thematicData\\{year}.txt"
    with open(fileName, "w") as file:
        file.write(f"{currNumOfGms}\n")

        # Formats and writes the top 10 countries to the file
        top10 = f"{top10Countries[0]},{countryData[top10Countries[0]]}"
        countries = top10Countries[1:10]
        for country in countries:
            top10 += f";{country},{countryData[country]}"
        top10 += "\n"
        file.write(top10)

        # Writes all of the country data into the file
        for gwCode, numOfGms in enumerate(countryData):
            file.write(f"{gwCode},{numOfGms}\n")

main()