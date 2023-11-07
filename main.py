import modules.convert
import modules.parse
import modules.execute
import sys

 # run this like py main.py test.bpp or python3 main.py test.bpp (depending on method of running python)
modules.execute.executeInstructions(modules.parse.parseTokens(modules.convert.convertFile(sys.argv[1])))
