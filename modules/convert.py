import sys

def toggle(input):# flip true -> false, false -> true
    if input == False:
        return True
    return False

def convertFile(FIQ): # takes in a raw text file, and returns a list of strings (tokens) that were separated by spaces. all other whitespace is removed.
    file = open(FIQ, "r")
    lines = []
    for x in file:
        lines.append(x)
    for i in range(len(lines)):# gets rid of \n at the end of all lines
        if i != len(lines)-1:
            lines[i] = lines[i][:-1]
    emptyCount = 0
    for i in range(len(lines)):# gets rid of empty lines
        if lines[i] == "":
            emptyCount+=1
    for i in range(emptyCount):
        lines.remove("")
    tokens = []

    allLines = ""
    for line in lines:
        allLines += " " + line
    # tokens = allLines.split(" ")

    tokenToAdd = ""
    inStringLit = False
    i = 0
    while i < len(allLines):
        if i > 1 and allLines[i] == "B":
            if allLines[i-1] == "b" and allLines[i-2] == "B":
                inStringLit = toggle(inStringLit)
        if allLines[i] == " " and inStringLit == False:
            tokens.append(tokenToAdd)
            tokenToAdd = ""
        else:
            tokenToAdd+=allLines[i]
        if i + 1 == len(allLines):# if at the end of the file
            tokens.append(tokenToAdd)
        i+=1

    # remove empty strings - meaning token list returned is every sequence of characters separated by whitespace, specifics ignored
    emptyCount = 0
    for token in tokens:# just empty line removal function from above
        if token == "":
            emptyCount+=1
    for i in range(emptyCount):
        tokens.remove("")
    # print(tokens)
    return tokens
