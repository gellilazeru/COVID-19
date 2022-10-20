# Function to load country, ID, sequence records from a file into a list of lists
# Input - FileName (string) of the file contains the records
# Output - a list of records
# Errors are not cheked for, file is expected to be in the correct format.
def LoadRecords(FileName):
    # The list of sequnce records to reutrn
    RecordList = []

    FIn = open(FileName, "r")

    # Read file line by line, to save memory.
    for Line in FIn:
        # Tokenize the file line on white space.
        # Record elements cannot contain white space.
        # Elemts in order are, the country code, unique ID, sequnce
        Tokens = Line.split()

        # Save the current record at the end of RecordList
        RecordList.append(Tokens)

    FIn.close()

    return RecordList


# Function to load the first sequence from a data file
# Format is is the same as for LoadRecords
# Input - FileName (string) of the file contains the records
# Output - the sequence (string)
# Errors are not checked for, one records is expected
def LoadSingleSequence(FileName):
    # Load All records, even though only the first is needed
    RecordData = LoadRecords(FileName)

    # only return the sequence from the first record.
    return RecordData[0][2]


# Function to calculate distance between two sequences
# Input - Two identical length sequences
# Output - sequence distance based on formula ( 1 - (Number of identities / Sequence Length))
# Checks for error and returns -1 if there is any error
def SequenceDistance(Pattern1, Pattern2) -> float:
    # variable for number of identical Nucleotides
    identicalNucleotides = 0
    # variable for total number of Nucleotides
    numberOfNucleotides = len(Pattern1)
    if len(Pattern1) != len(Pattern2):
        # return -1 and generate a warning if length of both the Patterns are not equal.
        print("Length of pattern should be same")
        return -1
    for i in range(len(Pattern1)):
        if Pattern1[i] == Pattern2[i]:
            # Increment identicalNucleotides variable if there is a common Nucleotide
            identicalNucleotides += 1
    # Calculating distance as specified in the question
    distance = 1.0 - float(identicalNucleotides / numberOfNucleotides)
    # Returning distance
    return distance


# Function to find and return the record with smallest SequenceDistance
# Input - Parameters, a single sequence and a list of records
# Output - returns sequence with minimum distance with Pattern passed as first Parameter
def FindClosestRecord(Pattern, RecordList) -> str:
    # stores the distances between Pattern and elements of RecordList
    listOfDistances = []
    # Looping over RecordList
    for record in RecordList:
        # Finding SequenceDistance and appending it to listOfDistances
        listOfDistances.append(SequenceDistance(Pattern1=Pattern, Pattern2=record[2]))
    # Finding minimum distance
    minimumDistance = min(listOfDistances)
    for i in range(len(RecordList)):
        if listOfDistances[i] == minimumDistance:
            # Return the sequence out of Records with minimum SequenceDistance with Patterm
            return RecordList[i][2]


# Function to find and return list of records with specified CountryName
# Input - Parameters, a single sequence and a list of records
# Output - returns sequence with minimum distance with Pattern passed as first Parameter
def FilterByCountry(RecordList, CountryName) -> list:
    # Returning list of Record with the Records which have Records as specified in the parameter using List Comprehension
    return [record for record in RecordList if record[0] == CountryName]


# Function identifies the closest matching pair of sequences between the origin country and the target country.
def PrintTransmitter(RecordList, OriginCountry, TargetCountry) -> None:
    # Filter Records for Origin
    OriginCountryRecords = FilterByCountry(RecordList=RecordList, CountryName=OriginCountry)
    # Filter Records for Target
    TargetCountryRecords = FilterByCountry(RecordList=RecordList, CountryName=TargetCountry)
    # List to store list of records which are closest for a particular record
    closestRecords = []
    # List to Store SequenceDistance
    listOfDistances = []
    # Looping over OriginCountryRecords
    for Record in OriginCountryRecords:
        closestRecords.append(FindClosestRecord(Record[2], TargetCountryRecords))
        listOfDistances.append(SequenceDistance(Record[2], closestRecords[len(closestRecords) - 1]))
    # Finding minimum distance
    minimumDistance = min(listOfDistances)
    for i in range(len(closestRecords)):
        # Printing the required output where the SequenceDistance is minimum
        if minimumDistance == listOfDistances[i]:
            # Printing Distance
            print("Distance : " + str(minimumDistance))
            # Printing OriginCountryRecordId
            print("OriginCountryRecordId : " + str(
                [record for record in OriginCountryRecords if record[2] == OriginCountryRecords[i][2]][0][1]))
            # Printing TargetCountryRecordId
            print("TargetCountryRecordId : " + str(
                [record for record in TargetCountryRecords if record[2] == closestRecords[i]][0][1]))


# Load all records from "Human-Covid19.txt" into a list of list, called Records
Records = LoadRecords("Human-Covid19.txt")

# Load only the Bat sequence into a string, BatSeq
BatSeq = LoadSingleSequence("Bat-Covid19.txt")

# Finding closest
closestRecordToBat = FindClosestRecord(Pattern=BatSeq, RecordList=Records)
print("Finding Closest Record To Bat")
# Finding Distance and printing it to the console
print("Distance :", SequenceDistance(Pattern1=BatSeq, Pattern2=closestRecordToBat))
# Finding RecordId and printing it to the console
print("RecordId : " + str(
    [record for record in Records if record[2] == closestRecordToBat][0][1]))
# Calling Print Transmitter function
print(
    "\nFinding Record of origin and target where EST is OriginCounty and UZB is TargetCountry (This may take some time)")
PrintTransmitter(RecordList=Records, OriginCountry="EST", TargetCountry="UZB")

