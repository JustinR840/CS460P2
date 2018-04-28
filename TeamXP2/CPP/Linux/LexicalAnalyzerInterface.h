#include "LexicalAnalyzer.h"


extern "C" LexicalAnalyzer* LexicalAnalyzer_New(char* filename);
extern "C" void LexicalAnalyzer_Destructor(LexicalAnalyzer* lex);
extern "C" token_type LexicalAnalyzer_GetToken(LexicalAnalyzer* lex);
extern "C" char* LexicalAnalyzer_GetTokenName(LexicalAnalyzer* lex, token_type t);
extern "C" char* LexicalAnalyzer_GetLexeme(LexicalAnalyzer* lex);
extern "C" void LexicalAnalyzer_FreeChar(char* seq);
extern "C" void LexicalAnalyzer_ReportError(LexicalAnalyzer* lex, char* str);

extern "C" char* LexicalAnalyzer_GetString(string str);

