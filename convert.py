import sys

def openFile(FIQ): # takes in a raw text file, and returns a list of strings (tokens) that were separated by spaces. all other whitespace is removed.
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
    for line in lines:
        lineTokens = line.split(" ")
        for token in lineTokens:
            tokens.append(token)# the token list here is every single sequence of characters separated by spaces - newlines ignored
    # remove empty strings - meaning token list returned is every sequence of characters separated by whitespace, specifics ignored
    for token in tokens:# just empty line removal function from above
        if token == "":
            emptyCount+=1
    for i in range(emptyCount):
        tokens.remove("")
    return tokens