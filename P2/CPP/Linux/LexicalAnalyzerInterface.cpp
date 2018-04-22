#include <string.h>
#include "LexicalAnalyzerInterface.h"


LexicalAnalyzer* LexicalAnalyzer_New(char* filename)
{
	return new LexicalAnalyzer(filename);
}

void LexicalAnalyzer_Destructor(LexicalAnalyzer* lex)
{
	delete lex;
}

token_type LexicalAnalyzer_GetToken(LexicalAnalyzer* lex)
{
	return lex->GetToken();
}

char* LexicalAnalyzer_GetTokenName(LexicalAnalyzer* lex, token_type t)
{
	string tmp = lex->GetTokenName(t);
	return LexicalAnalyzer_GetString(tmp);
}

char* LexicalAnalyzer_GetLexeme(LexicalAnalyzer* lex)
{
	string tmp = lex->GetLexeme();
	return LexicalAnalyzer_GetString(tmp);
}

char* LexicalAnalyzer_GetString(string str)
{
	// Remove underscore for linux?
	char* new_buf = strdup(&str[0]);
	return new_buf;
}

void LexicalAnalyzer_FreeChar(char* obj)
{
	free(obj);
};


void LexicalAnalyzer_ReportError(LexicalAnalyzer* lex, char* str)
{
	lex->ReportError(str);
}
