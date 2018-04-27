import urllib.request
import csv
import os
import math

## A few Notes:
##
## -The Month CSV file contains an extra comma at the end of each line, which can cause some errors if not accounted for
## -The Month and Day CSV differ in formating, as the monthly one displays Months with a 0 before ( such as 04/26 and not 4/26, line the day file)
##
## -These two problems might be because we're using the file 'eriePrelimCMo.csv' but there's also a 'eriePrelimMo.csv' which seems to be valid
##
## -The program expects the Monthly average water level to only have one entry. If that changes, it's easy to change functionality to accept a variable amount of lines/inputs

dir_path = os.path.dirname(os.path.realpath(__file__))
print("Downloading Monthly and Daily readings...")
monthURL = "https://www.glerl.noaa.gov/data/dashboard/data/levels/1918_PRES/eriePrelimCMo.csv"
urllib.request.urlretrieve(monthURL, (dir_path + "/month.csv"))

dayURL = "https://www.glerl.noaa.gov/data/dashboard/data/levels/1918_PRES/eriePrelimCDaily.csv"
urllib.request.urlretrieve(dayURL, (dir_path + "/day.csv"))
print("Download complete! Using files as input:")

dailyValues = {}
monthlyAvg = 0.0

#Opening both files and adding their data to a set.
print("Reading Day file...")
with open("day.csv") as csvFile:
    fileReader = csv.reader(csvFile)

    for line in fileReader:
        dailyValues.update({line[0]: line[1]})

print("Reading Month file...")
with open("month.csv") as csvFile:
    fileReader = csv.reader(csvFile)

    for line in fileReader:
        #Checking if line has elements. This would NOT have to be done if the CSV file was valid, so I suspect it does
        # not conform to CSV guidelines.
        if len(line) > 0:
            monthlyAvg = line[1]

dailyDeviation = {}
for item in dailyValues:
    daily = float(dailyValues.get(item))
    deviation = daily - float(monthlyAvg)
    dailyDeviation.update({item : deviation})

print("Daily deviation calculated! Writing to file: deviation.csv.")
w = csv.writer(open("deviation.csv", "w"))
w.writerow(["Date", "Deviation"])
for key, val in dailyDeviation.items():
    #Rounding the floats to two decimals as we write them to the file.
    w.writerow([key, (math.ceil(val*100)/100)])

