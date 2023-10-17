import modules.convert
import modules.parse
import modules.execute

modules.execute.executeInstructions(modules.parse.parseTokens(modules.convert.convertFile(input("File ? "))))
