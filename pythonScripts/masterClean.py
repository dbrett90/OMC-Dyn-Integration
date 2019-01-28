# title          : masterClean.py
# description    : Python Script which completely cleans original log files
# author         : Daniel Brett
# date           : December 3rd, 2018
# python_version : 3.6
# ==================================================
import random, math
import datetime
import time
import os, csv
import pycountry
from pycountry_convert import country_alpha2_to_continent_code

class masterClean(object):
    def __init__(self, inFile, outFile):
        self.inFile = inFile
        self.outFile = outFile

    #######################################################################
    ######################Generate Username Method#########################
    #######################################################################

    #Only need to use this method if there are no usernames attached to log files. Should only be used to Mock Data for testing purposes
    def genUsername(self):
        userList = ['mary.baker@oracle.com', 'john.smith@oracle.com', 'kevin.brown@oracle.com', 'jenna.brett@oracle.com', 'danny.brett@oracle.com']
        with open(self.inFile, 'rU') as csv_in, open(self.outFile, 'w') as csv_out:
            writer = csv.writer(csv_out, lineterminator = "\n")
            reader = csv.reader(csv_in)
            rows = [next(reader)]
            rows[0].insert(0, "Username")
            for line in reader:
                randUser = random.randint(0,len(userList)-1)
                line.insert(0, userList[randUser])
                rows.append(line)
            writer.writerows(rows)
        print("Usernames have been added.")
        print("\n")



    #######################################################################
    ######################Fill Blanks Method###############################
    #######################################################################
    def fillBlanks(self):
        #rename the file for output accordingly
        with open(self.inFile, 'rU') as csv_in, open(self.outFile, 'w') as csv_out:
            writer = csv.writer(csv_out, lineterminator = "\n")
            reader = csv.reader(csv_in)
            rows = [next(reader)]
            #row_count = sum(1 for row in reader)
            numCols = len(next(reader))
            for line in reader:
                for x in range(numCols):
                    if line[x]=="" or line[x]==None:
                        line[x] = "-"
                rows.append(line)
            writer.writerows(rows)
        print("File has been had blanks filled.")
        print("\n")
        csv_in.close()
        csv_out.close()
    ######################################################################
    ######################DeleteCols Method###############################
    ######################################################################
    def deleteCols(self):
        #Determine which columns are to be deleted and append to an array
        colArray = []
        flag = True
        while flag ==True:
            #Get the user to specify the columns they want to delete
            colNum = int(raw_input("What Column do you want to delete? "))-1
            colArray.append(colNum)
            cont = raw_input("do you have more columns you want to delete? (y/n)")
            if cont =="n":
                flag = False
        #VITALLY IMPORTANT. Reverse sort so there is no premature cell shifting.
        colArray.sort(reverse = True)
        #Read in the necessary logFiles
        with open(self.inFile, mode = 'r') as csv_in, open(self.outFile, mode = 'w') as csv_out:
            writer = csv.writer(csv_out, lineterminator = "\n")
            reader = csv.reader(csv_in)
            for row in reader:
                for col in colArray:
                    del row[col]
                writer.writerow(row)

        print("File has had columns deleted.")
        print("\n")
        csv_in.close()
        csv_out.close()
    #######################################################################
    ######################TimeStamp Methods################################
    #######################################################################

    def genTimeStamps(self, numStamps, difMins):
        timeStamps = []
        for rows in range(numStamps):
            #600000 corresponds to 10 minutes
            timeStamps.append(int(math.floor(1543849200+ rows*difMins)))
        return timeStamps

    def createStamps(self):
        numStamps = int(raw_input("How long is your file? (rows): "))
        difMins = int(raw_input("What should the difference between timestamps be? (mins): "))*60
        with open(self.inFile, 'rU') as csv_in, open(self.outFile, 'w') as csv_out:
            writer = csv.writer(csv_out, lineterminator = "\n")
            reader = csv.reader(csv_in)
            rows = [next(reader)]
            x=0
            timeStamps = self.genTimeStamps(numStamps, difMins)
            for line in reader:
                #Change the column here. By default set to first column
                line[0] = timeStamps[x]
                x+=1
                rows.append(line)
            writer.writerows(rows)
        print("File has been updated with new timestamps. Check your directory.")
        print("\n")
        csv_in.close()
        csv_out.close()

    #######################################################################
    ######################CONTINENT METHOD#################################
    #######################################################################

    def createContinentColumn(self):
        #Read in the necessary files
        with open(self.inFile, mode = 'rU') as csv_in, open(self.outFile, mode = 'w') as csv_out:
            writer = csv.writer(csv_out, lineterminator = "\n")
            reader = csv.reader(csv_in)
            rows = [next(reader)]
            numCols = len(next(reader))
            #Add Header
            rows[0].append("Continent Code")
            #Find the column with Country Code
            for row in range(len(rows)):
                for col in range(len(rows[row])):
                    #This is assuming the field is called country code (not case sensitive)
                    if rows[row][col].lower() == "country code":
                        countryCol = col
                    #getting rid of extraneous Europe tags. Issue with logs.
                    if rows[row][col].lower() == "country name":
                        nameCol = col
            #Let's add the new values to rows array
            #note: exemption is made for "-" here. This will only work if you have used
            #my other log standardization tools
            for line in reader:
                #below lines are specific to dyn files because some country names have
                #been mistakenly labeled "Europe". If Dataset does not have
                #this issue, can delete rows 155-157 as it is extraneous.
                if line[nameCol].lower()=="europe":
                    line[nameCol]="Finland"
                    rows.append(line)
                if line[countryCol]=="-":
                    line.append("-")
                    rows.append(line)
                else:
                    line.append(self.getContinent(line[countryCol]))
                    rows.append(line)
            writer.writerows(rows)
        print("File has been updated with Continent Codes")
        print("\n")
        csv_in.close()
        csv_out.close()

    #Function to get the Continent Code based off a country code
    def getContinent(self, countryCode):
        if countryCode=="EU":
            return "EU"
        return country_alpha2_to_continent_code(countryCode)


#######################################################################
######################GENERATE NEW FILES###############################
#######################################################################
fillBlanks = masterClean('../logFiles/dyn_newest_logs.csv', '../logFiles/dyn_data1.csv').fillBlanks()
deleteCols = masterClean('../logFiles/dummy_original_logs1.csv', '../logFiles/dyn_data2.csv').deleteCols()
overwrite= masterClean('../logFiles/dummy_original_logs2.csv', '../logFiles/dyn_data3.csv').createStamps()
addConts = masterClean('../logFiles/dummy_original_logs3.csv', '../logFiles/dyn_data4.csv').createContinentColumn()
addusers = masterClean('../logFiles/dummy_final.csv', '../logFiles/dyn_data_final.csv').genUsername()
