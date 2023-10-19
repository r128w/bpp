# takes in an instruction list from parse
# executes the code

def executeInstructions(instructions):
    # print("Instruction list:")
    print(instructions)
    # print("")
    currentIndex = 0
    
    while currentIndex < len(instructions):
        print(instructions[currentIndex])

        match(instructions[currentIndex][0]):
            case "print":
                print(getValue(instructions[currentIndex][1]))
            case "if":
                if getValue(instructions[currentIndex][1]) <= 0:
                    #TODO jump to matching "bB"
                    #<!!!> errorcase: malformed bbrackets
                    print("wip")
                

        currentIndex+=1


def getValue(input):# magic of recursion function
    # takes in a string or list and gets the value that list resolves to using recursion
    
    # base of the tree case
    if type(input) == int:
        return input
    
    if type(input) == str:# TODO variable support
        if input[0] == "\"" and input[-1] == "\"":# string literals
            return input[1:-1]
        # at this point it must be a variable
        varIndex = int(input[1])

    #by this point the input must be a list, meaning recursion should happen

    # <!!!> errorcase: list is malformed (not 3 items, doesnt contain operation, etc)
    match(input[1]):# perform the operations
        case "==":
            if getValue(input[0]) == getValue(input[2]):
                return 1
            return 0
        case "+":
            return getValue(input[0]) + getValue(input[2])# <!!!> errorcase: different types
        case "-":
            return getValue(input[0]) - getValue(input[2])# <!!!> errorcase: not numbers
        case "*":
            return getValue(input[0]) * getValue(input[2])# <!!!> errorcase: not numbers
        case "/":
            return getValue(input[0]) / getValue(input[2])# <!!!> errorcase: not numbers
