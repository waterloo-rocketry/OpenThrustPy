import csv

OUTPUT_CSV_TITLE = "output.csv"

def outputToDisk(headerArray, columns):
    if len(headerArray) != len(columns):
        raise RuntimeError("Length of output headers for csv file does"
                           + " not match length of output columns")
        return
    for column in columns:
        for c in columns:
            if len(c) != len(column):
                raise RuntimeError("Length of columns for csv file do"
                                   + " not match")
    for column in columns:
        length = len(column)
        break
    with open(OUTPUT_CSV_TITLE, 'w', newline='') as csvfile:
        outputWriter = csv.writer(csvfile, delimiter=',')
        outputWriter.writerow(headerArray)
        for i in range(length):
            outputWriter.writerow([column[i] for column in columns])

