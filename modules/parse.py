import modules.error


def groupParens(tokens):# takes in tokens, outputs tokens nested via b parens
    # ['brint', 'b', 'bar', '+' , 'bor', 'B'] -> ['brint', ['bar', '+', 'bor']]
    #<!!!.> errorcase: mismatched brackets
    output = []
    i = 0
    while i < len(tokens):
        if tokens[i] == "b":
            counter = 1
            lookAhead = 0
            while counter > 0:
                lookAhead+=1
                # TODOdone add check for mismatched brackets:
                # along the lines of before each of the iterations below checking if i + lookahead exceeds token list length

                if i + lookAhead >= len(tokens):
                    modules.error.throwError("Attempted to group mismatched brackets", False)

                if tokens[i + lookAhead] == "B":
                    counter -= 1
                elif tokens[i + lookAhead] == "b":
                    counter += 1
            output.append(groupParens(tokens[i+1:i + lookAhead]))
            i+=lookAhead
        else:
            output.append(tokens[i])
        i+=1
    return output

def CBtT(SIQ): # Convert Bokens to Tokens (String in Question)
# <!!> make sure this is only given strings (though that shouldnt be a problem)
# if string is not perfectly formatted as bumber, it will just return the string unchanged
    if SIQ[0:2] != "BB" and SIQ[0:3] != "BbB":
        return SIQ
    elif SIQ[0:2] == "BB":
        counter = 0
        for char in SIQ[2:]:
            if char == "b":
                counter+=1
            else:
                return SIQ
        return counter
    elif SIQ[-3:] == "BbB":
        return "\"" + SIQ[3:-3] + "\""
    return SIQ

def parseInBrackets(LIQ):# List in Question
    # parser used on a set of brackets in code: ["bum", "bore", "BBb"] - > ["bum", ">", 1]
    # should call itself on sublists
    if type(LIQ) != list:
        return LIQ# this should only operate on lists
    if len(LIQ) == 1:
        return LIQ[0]# if it's a list with one item, just return the item outside of brackets. this way, statements like "brint b BbBbogos bintedBbB B" and "brint BbBbogos bintedBbB" are equivalent
    for i in range(len(LIQ)):# convert all the bumbers to integers
        LIQ[i] = CBtT(LIQ[i])
        # switch around tokens
        match(LIQ[i]):
            case "blus":
                LIQ[i] = "+"
            case "binus":
                LIQ[i] = "-"
            case "bimes":
                LIQ[i] = "*"
            case "bivide":
                LIQ[i] = "/"
            case "bore":
                LIQ[i] = ">"
            case "bess":
                LIQ[i] = "<"
            case "biss":
                LIQ[i] = "=="
            case "band":
                LIQ[i] = "&"
            case "binput":
                LIQ[i] = "input"
            case "bot":
                LIQ[i] = "!"
            case "bat":
                LIQ[i] = "@" 
            case "bength":
                LIQ[i] = "len"
        if type(LIQ[i]) == list:# *recursion* for sub brackets
            LIQ[i] = parseInBrackets(LIQ[i])
    return LIQ

commandTerms = ["print", "if", "while", "bB", "Bb", "setVar", "setArray", "input", "+", "-", "*", "/", "!", "@", "<", ">", "==", "len"]#list of tokens that should not be replaced with ids

global variableNames
variableNames = []# to keep track of the variable ids and names -
    # first occuring variable is in variables[0], second in [1], etc
    # so in brint b bogos blus binted B, variables would be ["bogos", "binted"]
    # the variables var must be external to work with recursionwef
    # this could conflict with execute's variables[], so i changed it to variableNames 6/11/2023

def simplifyVariables(input):# inputs list of instructions, outputs same list with instances of variables replaced with "v<id>"
    output = input.copy() # for gods sake, why does python need to be so fancy with references
    
    for i in range(len(input)):
        
        if type(input[i]) == list:# recursively apply this function to every non-list item in every sublist
            output[i] = simplifyVariables(output[i])
            continue

        isVariable = True
        for term in commandTerms:
            if input[i] == term:
                isVariable = False

        if isVariable == False:
            continue# skip the token

        if type(input[i]) != str:# catch numbers
            continue# skip

        if input[i][0] == "\"" and input[i][-1] == "\"":# catch literal strings
            continue# skip
        
        # print("baba booey" + str(input) + str(variableNames))# WHY IS VARIABLENAMES FILLED WITH V0 V1 V2 WHAT

        tokenVarID = -1 # start at -1
        for j in range(len(variableNames)):# check if the variable's name is already in the list
            if input[i] == variableNames[j]:
                tokenVarID = j
                break

        if tokenVarID != -1:# if it is, use that id in the output
            output[i] = "v" + str(tokenVarID)
            continue
        
        output[i] = "v" + str(len(variableNames))# if the id came out -1 (not there), add it to the variable list
        variableNames.append(input[i])
        # print("aaa " + str(variableNames))
        continue
        
    return output

# instructions in a list are formatted so each operation is its own separate sublist, and bbrackets are strings:
# [["if", [1, ">", 0]], "bB", ["print", "\"bogos binted\""], "Bb"]
def parseTokens(tokens):# takes in raw tokens, outputs instructions
    # step one: search through for "b" tokens, and group up lists accordingly
    # ["bif", "b", "bexample", "biss", "BBbb", "B"] -> ["bif", ["bexample", "biss", "BBbb"]]
    tokens = groupParens(tokens)
    for i in range(len(tokens)):
        tokens[i] = parseInBrackets(tokens[i])
    output = []
    i = 0

    primedForBisorBat = False

    while i < len(tokens):# TODOdone make skipping over tokens not possible by keeping track of any tokens not included in the output somehow
        # print(i)
        # print(tokens[i])
        match(tokens[i]):#<!!!.> errorcase: function without argument is written (ie ending the file with brint)
            case "brint":
                if i + 1 >= len(tokens):
                    modules.error.throwError("Brint statement called without argument", False)
                output.append(["print", CBtT(tokens[i + 1])])
                i+=2
                continue
            case "bif":
                if i + 1 >= len(tokens):
                    modules.error.throwError("Bif statement called without argument", False)
                output.append(["if", CBtT(tokens[i + 1])])
                i+=2
                continue
            case "boop":
                if i + 1 >= len(tokens):
                    modules.error.throwError("Boop statement called without argument", False)
                output.append(["while", CBtT(tokens[i + 1])])
                i+=2
                continue
            case "bB":
                output.append("bB")
                i+=1
                continue
            case "Bb":
                output.append("Bb")
                i+=1
                continue
            case "bis":
                if i - 1 < 0:
                    modules.error.throwError("Bis statement called without variable name", False)
                if i + 1 >= len(tokens):
                    modules.error.throwError("Bis statement called without value", False)

                if primedForBisorBat == False: # needs to have been a non-function token skipped last iteration
                    modules.error.throwError("Bis statement called without variable name", False)

                output.append(["setVar", CBtT(tokens[i - 1]), CBtT(tokens[i + 1])])
                primedForBisorBat = False
                i+=2
                continue
            case "bat":

                if i + 3 >= len(tokens):
                    modules.error.throwError("Bat statement called without sufficient arguments", False)
                if i - 1 < 0:
                    modules.error.throwError("Bat statement called without first argument", False)

                if primedForBisorBat == False:
                    modules.error.throwError("Bat statement called without first argument", False)

                if tokens[i + 2] != "bis":
                    modules.error.throwError("Malformed Bat statement - no matching Bis", False)

                output.append(["setArray", CBtT(tokens[i - 1]), CBtT(tokens[i + 1]), CBtT(tokens[i + 3])])# <!!!.> spit an error if tokens[i + 2] is not bis
                primedForBisorBat = False
                i+=4
                continue

        if primedForBisorBat == True:
            modules.error.throwError("Argument given without function - Bis or Bat statement expected", False)

        primedForBisorBat = True # after this is et true, there needs to be a bis or bat in the next token, or error
        # TODOdone only have this run if tokens[i + 1] isnt bat or bis:
        # print("Hey! your code bad")# <!!!> this shouldnt be reached (unless there is a bis or a bat next)
        i+=1 # to prevent infinite loops
    output=simplifyVariables(output)
    # print(output)
    return output
