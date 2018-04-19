import SyntacticalAnalyzer as SA
from sys import argv, exit


def main():
	# TODO: Detect python version? We have a minimum of 3.6 because of auto() in Tokens.py
	if(len(argv) < 2):
		print("format: " + argv[0] + " <filename>")
		exit(1)

	syn = SA.SyntacticalAnalyzer(argv[1])
	syn.parse()


main()