import LexicalAnalyzer as LA
import SyntacticalAnalyzer as SA
from sys import argv, exit
from Tokens import Token


def main():
	# TODO: Detect python version? We have a minimum of 3.6
	if(len(argv) < 2):
		print("format: " + argv[0] + " <filename>")
		exit(1)

	lex = LA.LexicalAnalyzer(argv[1].encode("utf-8"))
	syn = SA.SyntacticalAnalyzer(lex)

	ct = lex.getToken()

	while(ct != Token.EOF_T):
		print(lex.getTokenName(ct))
		ct = lex.getToken()

	#syn.parse()



















main()