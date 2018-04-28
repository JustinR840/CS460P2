#pragma once

#ifdef LEXICALANALYZER_EXPORTS
#define LEXICALANALYZER_API __declspec(dllexport)
#else
#define LEXICALANALYZER_API __declspec(dllimport)
#endif

#include "LexicalAnalyzer.h"


extern "C" LEXICALANALYZER_API LexicalAnalyzer* LexicalAnalyzer_New(char* filename);
extern "C" LEXICALANALYZER_API void LexicalAnalyzer_Destructor(LexicalAnalyzer* lex);
extern "C" LEXICALANALYZER_API token_type LexicalAnalyzer_GetToken(LexicalAnalyzer* lex);
extern "C" LEXICALANALYZER_API char* LexicalAnalyzer_GetTokenName(LexicalAnalyzer* lex, token_type t);
extern "C" LEXICALANALYZER_API char* LexicalAnalyzer_GetLexeme(LexicalAnalyzer* lex);
extern "C" LEXICALANALYZER_API void LexicalAnalyzer_FreeChar(char* seq);

// This is a helper function, we don't need to include it in the C interface (I mean I guess
// it's still there in the library but ctypes can't access it)
char* LexicalAnalyzer_GetString(string str);

