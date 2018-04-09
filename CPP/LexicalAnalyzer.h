#ifndef LEX_H
#define LEX_H

#include <iostream>
#include <fstream>

using namespace std;

enum token_type
{
	NONE = -1,
	ZILCH,
	IDENT_T,
	NUMLIT_T,
	STRLIT_T,
	LISTOP_T,
	CONS_T,
	IF_T,
	COND_T,
	AND_T,
	OR_T,
	NOT_T,
	DEFINE_T,
	ELSE_T,
	MODULO_T,
	DISPLAY_T,
	NEWLINE_T,
	NUMBERP_T,
	LISTP_T,
	ZEROP_T,
	NULLP_T,
	SYMBOLP_T,
	STRINGP_T,
	PLUS_T,
	MINUS_T,
	DIV_T,
	MULT_T,
	EQUALTO_T,
	GT_T,
	LT_T,
	GTE_T,
	LTE_T,
	LPAREN_T,
	RPAREN_T,
	QUOTE_T,
	EOF_T,
	ERROR_T,
	NUM_TOKENS
};

class LexicalAnalyzer 
{
    public:
		LexicalAnalyzer (char * filename);
		~LexicalAnalyzer ();
		token_type GetToken ();
		string GetTokenName (token_type t) const;
		string GetLexeme () const;
		void ReportError (const string & msg);

		void ListingOutput(const string & msg);
		void TokenOutput(const string & msg);
		void DebugOutput(const string & msg);
		int NumErrors();
    private:
		int strType(int currentState, char c);
		void tryGetNewLine();
		void trySetToken();

		ifstream input;
		ofstream listingFile;
		ofstream tokenFile;
		ofstream debugFile;
		token_type token;
		string line;
		int linenum;
		int pos;
		string lexeme;
		int errors;
};


extern "C"
{
	LexicalAnalyzer* LexicalAnalyzer_new(char* filename) { return new LexicalAnalyzer(); }
	void 

	LexicalAnalyzer (char * filename);
	~LexicalAnalyzer ();
	token_type GetToken ();
	string GetTokenName (token_type t) const;
	string GetLexeme () const;
	void ReportError (const string & msg);

	void ListingOutput(const string & msg);
	void TokenOutput(const string & msg);
	void DebugOutput(const string & msg);
	int NumErrors();
	
	int strType(int currentState, char c);
	void tryGetNewLine();
	void trySetToken();














	
#endif
