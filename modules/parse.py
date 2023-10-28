
def groupParens(tokens):# takes in tokens, outputs tokens nested via b parens
    # ['brint', 'b', 'bar', '+' , 'bor', 'B'] -> ['brint', ['bar', '+', 'bor']]
    #<!!!> errorcase: mismatched brackets
    output = []
    i = 0
    while i < len(tokens):
        if tokens[i] == "b":
            counter = 1
            lookAhead = 0
            while counter > 0:
                lookAhead+=1
                # TODO add check for mismatched brackets:
                # along the lines of before each of the iterations below checking if i + lookahead exceeds token list length
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
        if type(LIQ[i]) == list:# *recursion* for sub brackets
            LIQ[i] = parseInBrackets(LIQ[i])
    return LIQ

commandTerms = ["print", "if", "while", "bB", "Bb", "setVar", "input", "+", "-", "*", "/", "!", "@", "<", ">", "=="]#list of tokens that should not be replaced with ids

variables = []# to keep track of the variable ids and names -
    # first occuring variable is in variables[0], second in [1], etc
    # so in brint b bogos blus binted B, variables would be ["bogos", "binted"]
    # the variables var must be external to work with recursion

def simplifyVariables(input):# inputs list of parsed tokens, outputs same list with instances of variables replaced with "v<id>"
    output = input
    
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
        
        tokenVarID = -1 # start at -1
        for j in range(len(variables)):# check if the variable's name is already in the list
            if input[i] == variables[j]:
                tokenVarID = j
                break

        if tokenVarID != -1:# if it is, use that id in the output
            output[i] = "v" + str(tokenVarID)
            continue
        
        output[i] = "v" + str(len(variables))# if the id came out -1 (not there), add it to the variable list
        variables.append(input[i])

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
    while i < len(tokens):# TODO make skipping over tokens not possible by keeping track of any tokens not included in the output somehow
        # print(i)
        # print(tokens[i])
        match(tokens[i]):#<!!!> errorcase: function without argument is written (ie ending the file with brint)
            case "brint":
                output.append(["print", CBtT(tokens[i + 1])])
                i+=2
                continue
            case "bif":
                output.append(["if", CBtT(tokens[i + 1])])
                i+=2
                continue
            case "boop":
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
                output.append(["setVar", CBtT(tokens[i - 1]), CBtT(tokens[i + 1])])
                i+=2
                continue
        print("Hey! your code bad")# this shouldnt be reached
        i+=1
    output=simplifyVariables(output)
    return output
