# takes in a list of instructions from parse.py
# executes the code

# TODO function support by giving executeinstructions a return value and recursion

import modules.utilities

def executeInstructions(instructions):
    # print("Instruction list:")
    # print(instructions)
    # print("")
    currentIndex = 0
    
    while currentIndex < len(instructions):
        # print(instructions[currentIndex])

        match(instructions[currentIndex][0]):#<!!!> if instructions[currentIndex] is an int (somehow) that would throw a type error - i dont think thats even possible though
            case "print":
                print(getValue(instructions[currentIndex][1]))
            case "if":
                if getValue(instructions[currentIndex][1]) <= 0:# <!!!> errorcase: bif <string> will throw a type error
                    #TODO jump to matching "Bb"
                    #<!!!> errorcase: malformed bbrackets
                    # print("wip")
                    bbracketCounter = 1
                    forwardOffset = 1
                    while bbracketCounter > 0:# <!!!> assumes that the instruction directly after "if" is always a bB, could cause errors
                        forwardOffset+=1
                        if instructions[currentIndex+forwardOffset] == "bB":# index + offset could lead to errors if out of bounds, which would happen with malformed bbrackets
                            bbracketCounter+=1
                        elif instructions[currentIndex+forwardOffset] == "Bb":
                            bbracketCounter-=1
                    currentIndex+=forwardOffset


                

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
    # need special case for bot and binput
    if len(input) == 2:
        match(input[0]):
            case "input":
                return modules.utilities.getInput(getValue(input[1]))# TODO this will always return a string, add a check to make it return a number if inputted value can be int()ed or float()ed - new getInput() function or smt?
            case "!":
                if getValue(input[1]) > 0:
                    return 0
                return 1
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
        case ">":
            if getValue(input[0]) > getValue(input[2]):# <!!!> errorcase: not numbers
                return 1
            return 0
        case "<":
            if getValue(input[0]) < getValue(input[2]): # <!!!> errorcase: not numbers
                return 1
            return 0
        case "&":
            if getValue(input[0]) > 0 and getValue(input[2]) > 0: # <!!!> errorcase: not numbers
                return 1
            return 0
        case "@":
            return getValue(input[0])[getValue(input[2])] # <!!!> getValue(input[0]) not a str or a list
        
