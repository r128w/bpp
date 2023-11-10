# takes in a list of instructions from parse.py
# executes the code

# TODO function support by giving executeinstructions a return value and recursion

# TODO have a debug mode or something as an option that prints out tokens parsed and executed, etc

import modules.utilities
import modules.error

variables = []

def executeInstructions(instructions):
    # print("Instruction list:")
    # print(instructions)
    # print("")
    currentIndex = 0
    
    while currentIndex < len(instructions):
        # print(instructions[currentIndex])

        match(instructions[currentIndex][0]):#<!!> if instructions[currentIndex] is an int (somehow) that would throw a type error - i dont think thats even possible though
            case "print":
                print(getValue(instructions[currentIndex][1]))

            case "if":

                argument = getValue(instructions[currentIndex][1])

                if type(argument) != int and type(argument) != float:
                    modules.error.throwError("Bif statement attempted to evaluate a non-numeric type", False)

                if argument <= 0:# <!!!.> errorcase: bif <string> will throw a type error
                    #TODOdone jump to matching "Bb"
                    #<.!!!> errorcase: malformed bbrackets (no matching bbracket to skip to)
                    # print("wip")
                    bbracketCounter = 1 
                    forwardOffset = 1
                    if currentIndex + 1 >= len(instructions):
                        modules.error.throwError("Bif statement attempted to skip to BBrackets that do not exist", False)
                    if instructions[currentIndex+1] != "bB":
                        modules.error.throwError("Bif statement not followed by a set of BBrackets", False)
                    while bbracketCounter > 0:# <!!!.> assumes that the token directly after "if" is always a bB, could cause errors
                        forwardOffset+=1
                        if currentIndex+forwardOffset >= len(instructions):
                            modules.error.throwError("Bif statement attempted to skip to BBrackets that do not exist", False)
                        if instructions[currentIndex+forwardOffset] == "bB":# index + offset could lead to errors if out of bounds, which would happen with malformed bbrackets
                            bbracketCounter+=1
                        elif instructions[currentIndex+forwardOffset] == "Bb":
                            bbracketCounter-=1
                    currentIndex+=forwardOffset
            # case "back":
            #     return getValue(instructions[currentIndex][1]) # functionality for functions (if i so wish)
            case "while":
                # similar to if, but backwards
                if getValue(instructions[currentIndex][1]) > 0:# if the argument is true, go back
                    bbracketCounter = 1
                    backwardOffset = 1
                    while bbracketCounter > 0:# <!!!> assumes that token directly after "boop" is Bb, could cause error
                        backwardOffset+=1
                        currentToken = instructions[currentIndex-backwardOffset]
                        if currentToken == "Bb":
                            bbracketCounter+=1
                        elif currentToken == "bB":
                            bbracketCounter-=1
                    currentIndex-=backwardOffset

            case "setVar":
                varName = instructions[currentIndex][1] # <!!!> expects a string formatted like v0 or v82 (v<number>), anything else wont work
                varID = int(varName[1:]) # chops off the v
                # print(varID)
                varValue = getValue(instructions[currentIndex][2])

                while varID >= len(variables): # <!!> if v4 is defined before v3 (for some reason, not even sure if possible (it is possible)), v3 will be initialized as None
                    variables.append(None)

                variables[varID] = varValue # this is very nice

            case "setArray":
                arrayName = instructions[currentIndex][1]
                arrayID = int(arrayName[1:]) # chops off v, very similar to above

                arrayIndex = getValue(instructions[currentIndex][2])
                valueToSet = getValue(instructions[currentIndex][3])

                # check this array even exists yet, similar to above

                while len(variables) <= arrayID: # as above, if attempting to define an array in an index that hasnt been filled up to yet, initialize lower vars as None
                    variables.append(None)

                if type(variables[arrayID]) != list:
                    # if the var isnt an array yet, make it one with its current value at index 0
                    variables[arrayID] = [variables[arrayID]]

                while arrayIndex >= len(variables[arrayID]): # if the array is being set at a point beyond its bounds, lengthen the array with Nones
                    variables[arrayID].append(None)

                variables[arrayID][arrayIndex] = valueToSet # clean and nice


        currentIndex+=1



def getValue(input):# magic of recursion function
    # takes in a string or list and gets the value that list resolves to using recursion
    
    # base of the tree case
    if type(input) == int:
        return input

    if type(input) == float:
        return input
    
    if type(input) == str:

        if input[0] == "\"" and input[-1] == "\"":# returns string literals as the string inside the quotes
            return input[1:-1]
        # at this point it must be a variable
        varIndex = int(input[1:])# <!!!.> assumes variable has been defined, and the variable list is long enough to not throw an out of bounds error - must catch undefined vars

        if len(variables) <= varIndex:
            modules.error.throwError("Variable value accessed without being defined", False)# TODO provide variable name?
        if variables[varIndex] == None:# None cannot be assigned to variable in code, so a var being none would mean it is undefined
            modules.error.throwError("Variable value accessed without being defined", False)

        return variables[varIndex]

    # by this point the input must be a list, meaning recursion should happen
    if type(input) != list:
        modules.error.throwError("How did you get the data type " + str(type(input)) + " to appear? Impressive.", True)

    # <!!!> errorcase: list is malformed (not 3 items, doesnt contain operation, etc)
    # need special case for bot and binput
    if len(input) == 2:
        match(input[0]):
            case "input":
                return modules.utilities.getInput(getValue(input[1]))# TODOdone this will always return a string, add a check to make it return a number if inputted value can be int()ed or float()ed - new getInput() function or smt?
            case "!":
                argument = getValue(input[1])

                if type(argument) != int and type(argument) != float:
                    modules.error.throwError("Attempted to invert non-invertible type", False)
                    
                if argument > 0:# <!!!.> if its not comparable to 0
                    return 0
                return 1
            case "len":
                argument = getValue(input[1])

                if type(argument) != str and type(argument) != list:
                    modules.error.throwError("Attempted to get length of non-string or array", False)

                return len(argument)#<!!!.> if type of input[1] isnt a string/list

    arg1 = getValue(input[0])
    arg2 = getValue(input[2])

    match(input[1]):# perform the operations
        case "==":# works regardless of data types

            if arg1 == arg2:
                return 1
            return 0 #<!!> attention: biss and band are two different functions!!! biss checks for literal similarity, band just checks if they're both above 0

        case "+":

            if type(arg1) != type(arg2):
                modules.error.throwError("Attempted to add two different types", False)

            if type(arg1) != str and type(arg1) != int and type(arg1) != float:
                modules.error.throwError("Attempted to add non-summable type", False)

            return arg1 + arg2# <!!!.> errorcase: different types

        case "-":

            if (type(arg1) != int and type(arg1) != float) or (type(arg2) != int and type(arg2) != float):
                modules.error.throwError("Attempted to subtract non-numeric types", False)

            return arg1 - arg2# <!!!.> errorcase: not numbers

        case "*":
        
            if (type(arg1) != int and type(arg1) != float) or (type(arg2) != int and type(arg2) != float):
                modules.error.throwError("Attempted to multiply non-numeric types", False)

            return arg1 * arg2# <!!!.> errorcase: not numbers

        case "/":
        
            if (type(arg1) != int and type(arg1) != float) or (type(arg2) != int and type(arg2) != float):
                modules.error.throwError("Attempted to divide non-numeric types", False)

            if arg2 == 0:
                modules.error.throwError("Attempted to divide by zero", False)

            return arg1 / arg2# <!!!.> errorcase: not numbers

        case ">":
        
            if (type(arg1) != int and type(arg1) != float) or (type(arg2) != int and type(arg2) != float):
                modules.error.throwError("Attempted to compare non-numeric types", False)

            if arg1 > arg2:# <!!!.> errorcase: not numbers
                return 1
            return 0

        case "<":
        
            if (type(arg1) != int and type(arg1) != float) or (type(arg2) != int and type(arg2) != float):
                modules.error.throwError("Attempted to compare non-numeric types", False)

            if arg1 < arg2: # <!!!.> errorcase: not numbers
                return 1
            return 0

        case "&":

            if (type(arg1) != int and type(arg1) != float) or (type(arg2) != int and type(arg2) != float):
                modules.error.throwError("Attempted to compare non-numeric types", False)

            if arg1 > 0 and arg2 > 0: # <!!!.> errorcase: not numbers
                return 1
            return 0

        case "@":

            if type(arg1) != str and type(arg1) != list:
                modules.error.throwError("Attempted to fetch value at index from a non-indexable type", False)
            
            if type(arg2) != int:
                modules.error.throwError("Attempted to fetch value at non-integer index", False)

            if len(arg1) <= arg2:
                modules.error.throwError("Attempted to fetch value outside of bounds", False)

            # <!!!.> assumes arg2 is within bounds
            return arg1[arg2] # <!!!.> getValue(input[0]) not a str or a list or arg2 not an int
        
