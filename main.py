import modules.convert
import modules.parse

# goes through all tokens in a given file, and prints the tokens grouped by their parentheses ("b" and "B")
print(modules.parse.groupParens(modules.convert.openFile(input("File ? "))))
