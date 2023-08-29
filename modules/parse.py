
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

def CACBTN(SIQ): # Check And Convert Bs To Number (String in Question)
# if string is not perfectly formatted as bumber, it will just return the string unchanged
    if SIQ[0:2] != "BB":
        return SIQ
    else:
        counter = 0
        for char in SIQ[2:]:
            if char == "b":
                counter+=1
            else:
                return SIQ
        return counter

def parseInBrackets(LIQ):# List in Question
    # parser used on a set of brackets in code: ["bum", "bore", "BBb"] - > ["bum", ">", 1]
    if type(LIQ) != list:
        return LIQ# this should only operate on lists
    if len(LIQ) == 1:
        return LIQ[0]# if it's a list with one item, just return the item outside of brackets. this way, statements like "brint b "bogos binted" B" and "brint "bogos binted"" are equivalent
    for i in range(len(LIQ)):# convert all the bumbers to integers
        LIQ[i] = CACBTN(LIQ[i])
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
                LIQ[i] = "="
            case "band":
                LIQ[i] = "&"
            case "binput":
                LIQ[i] = "input"
            case "bot":
                LIQ[i] = "!"
            case "bat":
                LIQ[i] = "@" 
    return LIQ


# instructions in a list are formatted so each operation is its own separate sublist, and bbrackets are strings:
# [["if", [1, ">", 0]], "bB", ["print", "\"bogos binted\""], "Bb"]
def parseTokens(tokens):# takes in raw tokens, outputs instructions
    # step one: search through for "b" tokens, and group up lists so that
    tokens = groupParens(tokens)
    for i in range(len(tokens)):
        tokens[i] = parseInBrackets(tokens[i])
    output = []
    i = 0
    while i < len(tokens):
        match(tokens[i]):
            case "brint":
                output.append(["print", CACBTN(tokens[i + 1])])
                i+=2
                continue
            case "bif":
                output.append(["if", CACBTN(tokens[i + 1])])
                i+=2
                continue
            case "boop":
                output.append(["while", CACBTN(tokens[i + 1])])
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
                output.append(["setVar", CACBTN(tokens[i - 1]), CACBTN(tokens[i + 1])])
                i+=2
                continue
        i+=1
    return output
