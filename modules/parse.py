
def groupParens(tokens):# takes in tokens, outputs tokens nested via b parens
    # ['brint', 'b', 'bar', '+' , 'bor', 'B'] -> ['brint', ['bar', '+', 'bor']]
    output = []
    i = 0
    while i < len(tokens):
        if tokens[i] == "b":
            counter = 1
            lookAhead = 0
            while counter > 0:
                lookAhead+=1
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

commandTerms = ["print", "if", "while", "bB", "Bb", "setVar", "input", "+", "-", "*", "/", "!", "@", "<", ">"]#list of tokens that should not be replaced with ids
def simplifyVariables(input):# inputs list of parsed tokens, outputs same list with instances of variables replaced with "v<id>"
    return

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
    while i < len(tokens):
        match(tokens[i]):
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
        i+=1
    return output

