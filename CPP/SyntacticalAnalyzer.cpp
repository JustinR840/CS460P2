#include <iostream>
#include <iomanip>
#include <fstream>
#include <cstring>
#include <sstream>
#include "SyntacticalAnalyzer.h"

using namespace std;

SyntacticalAnalyzer::SyntacticalAnalyzer (char * filename)
{
	lex = new LexicalAnalyzer (filename);
	token_type t;
	while ((t = lex->GetToken()) != EOF_T)
	{
		if (t != NONE)
		{
			// get a token
			// write its name to the .p1 file
			// write the corresponding lexeme to the .p1 file
			string token_str = lex->GetTokenName(t);
			string lexeme = lex->GetLexeme();
			stringstream ss;
			ss << "\t" << setw(15) << left << token_str << lexeme << endl;
			lex->TokenOutput(ss.str());
		}
	}

	stringstream ss;
	ss << "\t" << setw(15) << left << lex->GetTokenName(t) << endl;
	lex->TokenOutput(ss.str());

	cout << to_string(lex->NumErrors()) << " errors found in input file" << endl;
}

SyntacticalAnalyzer::~SyntacticalAnalyzer ()
{
	delete lex;
}
