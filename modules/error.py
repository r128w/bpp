
# this file is where all the errors get thrown
# basically another file imports modules.error
# then can call modules.error.throwError(message)

import sys

def throwError(message, isBig): # message is the message returned, isBig is whether this is an impressive error to encounter or not
    if isBig:
        print("Congratulations. I don't know how you got here.")
    print("<!> Error: " + message)
    sys.exit()# halt entire program
