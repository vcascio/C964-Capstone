import json as js
import csv
import pandas as pd
from pandas.plotting import scatter_matrix
from matplotlib import pyplot



def ConvertHeightToInches(height):
    heightArray = height.split(' ')
    heighthFeet = heightArray[0].strip("ft")

    if heightArray.__len__() == 1:
        return int(heighthFeet) * 12
    else:
        heighthinches = heightArray[1].strip("in")

        return int(heighthFeet) * 12 + int(heighthinches)

def ConvertDataToCsv(fromFilePath, headers, toFilePath, missingFieldsAllowed, itemId = 0):
    with open(toFilePath, 'w', newline='') as outCsvFile:
        csvWriter = csv.writer(outCsvFile)
        csvWriter.writerow(headers)
        with open(fromFilePath, 'r') as openFile:
            fileContent = js.load(openFile)
            for i in fileContent["FitList"]:
                tempList = [""] * headers.__len__()
                dataCount = 0
                for j in i.keys(): # iterate over each fitting
                    if j == "item_id": # filter to only one item
                        if itemId != 0:
                            if i[j] != itemId:
                                break
                    if j == "fit":
                        if i[j] != "fit":
                            break # do not include records that do not fit
                    if j == "hips":
                        i[j] = i[j].split(".")[0]
                    if j == "height":
                        i[j] = ConvertHeightToInches(i[j])
                    if headers.__contains__(j):
                        tempList[headers.index(j)] = i[j]
                        dataCount = dataCount + 1
                if dataCount >= headers.__len__()-missingFieldsAllowed:
                    csvWriter.writerow(tempList)

jdkjls = []
jdkjls.append()
sourceFileUri = r"Data\modcloth_final_data_medium.json"
allOutputFileUri = r"Data\modcloth_final_data_all.csv"

outputFileUri = r"Data\modcloth_final_data_medium.csv"
headers = [ "item_id", "waist", "cup size", "hips", "bra size", "length", "height", "fit", "size" ]
missingFieldsAllowed = 0
itemId = "125442"

userHeaders = [ "waist", "hips", "bra size", "size" ]
ConvertDataToCsv(sourceFileUri, userHeaders, outputFileUri, missingFieldsAllowed)
ConvertDataToCsv(sourceFileUri, headers, allOutputFileUri, missingFieldsAllowed)

# viewing the data
df = pd.read_csv(allOutputFileUri)
df2 = pd.read_csv(outputFileUri)

print("Scatter Plot of All Data")
scatter_matrix(df)
pyplot.show()

print("Scatter Plot of Data for Item ID: " + str(itemId))
scatter_matrix(df2)
pyplot.show()