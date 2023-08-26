
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

# instructions in a list are formatted so each operation is its own separate sublist, and bbrackets are strings:
# [["if", ["1", ">", "0"]], "bB", ["print", "\"bogos binted\""], "Bb"]
def parseTokens(tokens):# takes in raw tokens, outputs instructions
    # step one: search through for "b" tokens, and group up lists so that
    tokens = groupParens(tokens)
    output = []
    i = 0
    while i < len(tokens):
        match(tokens[i]):
            case "brint":
                output.append(["print", tokens[i + 1]])
                i+=2
                continue
            case "bif":
                output.append(["if", tokens[i + 1]])
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
        i+=1
    return output
