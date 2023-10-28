# file for all the assorted functions i might need throughout the project



def listContains(inputList, inputItem):# also works with strings and chars
    for item in inputList:
        if item == inputItem:
            return True
    return False


digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

def isInt(string):# checks if a string can be int()ed
    for char in string:
        if listContains(digits, char) == False:
            return False
    return True

def isFloat(string):# checks if a string can be float()ed
    for char in string:
        if listContains(digits+["."], char) == False:# <!!!> multiple decimal points trips it up
            return False
    return True


def getInput(prompt):# takes a string as a prompt, and returns user input - but the input is a float or int if necessary
    rawInput = input(prompt)
    if isInt(rawInput):
        return int(rawInput)
    if isFloat(rawInput):
        return float(rawInput)
    return rawInput
