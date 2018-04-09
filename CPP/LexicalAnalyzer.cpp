#include <iomanip>
#include <cstdlib>
#include <string>
#include <map>
#include <algorithm>
#include "LexicalAnalyzer.h"

using namespace std;

const int WHITESPACE_STATE = 16;
const int ALPHA_STATE = 15;
const int NUMBER_STATE = 20;
const int NEWLINE_STATE = 21;
const int UNKNOWN_STATE = 22;

static string token_names[] = {
	"",
	"IDENT_T",
	"NUMLIT_T",
	"STRLIT_T",
	"LISTOP_T",
	"CONS_T",
	"IF_T",
	"COND_T",
	"AND_T",
	"OR_T",
	"NOT_T",
	"DEFINE_T",
	"ELSE_T",
	"MODULO_T",
	"DISPLAY_T",
	"NEWLINE_T",
	"NUMBERP_T",
	"LISTP_T",
	"ZEROP_T",
	"NULLP_T",
	"SYMBOLP_T",
	"STRINGP_T",
	"PLUS_T",
	"MINUS_T",
	"DIV_T",
	"MULT_T",
	"EQUALTO_T",
	"GT_T",
	"LT_T",
	"GTE_T",
	"LTE_T",
	"LPAREN_T",
	"RPAREN_T",
	"QUOTE_T",
	"EOF_T",
	"ERROR_T"
};

static map<char, int> mp = {
	{ '/', 0 },
	{ '*', 1 },
	{ '=', 2 },
	{ '>', 3 },
	{ '<', 4 },
	{ '(', 5 },
	{ ')', 6 },
	{ '\'', 7 },
	{ '"', 8 },
	{ 'c', 9 },
	{ 'a', 10 },
	{ 'd', 11 },
	{ 'r', 12 },
	{ '_', 13 },
	{ '?', 14 },
	{ '+', 17 },
	{ '-', 18 },
	{ '.', 19 }
};

static map<string, token_type> predicates = {
	{ "number?", NUMBERP_T },
	{ "list?", LISTP_T },
	{ "symbol?", SYMBOLP_T },
	{ "zero?", ZEROP_T },
	{ "null?", NULLP_T },
	{ "string?", STRINGP_T }
};

static map<string, token_type> keywords = {
	{ "cons", CONS_T },
	{ "if", IF_T },
	{ "cond", COND_T },
	{ "and", AND_T },
	{ "or", OR_T },
	{ "not", NOT_T },
	{ "define", DEFINE_T },
	{ "else", ELSE_T },
	{ "modulo", MODULO_T },
	{ "display", DISPLAY_T },
	{ "newline", NEWLINE_T }
};

static token_type no_backup[] = { DIV_T, MULT_T, GTE_T, LTE_T, RPAREN_T, LPAREN_T, QUOTE_T, EQUALTO_T, ERROR_T, STRLIT_T };

static int dfa[13][23] = {
//					0				1				2				3				4				5				6				7				8				9				10				11				12				13				14				15				16				17				18				19				20				21				22
//					/				*				=				>				<				(				)				'				"				c				a				d				r				_				?				alpha			ws				+				-				.				number			\n				unknown
/*0 starting*/	{ -DIV_T	,	-MULT_T		,	-EQUALTO_T	,		1		,		2		,	-LPAREN_T	,	-RPAREN_T	,	-QUOTE_T	,		3		,		9		,		12		,		12		,		12		,	-ERROR_T	,	-ERROR_T	,		12		,		0		,		4		,		5		,		7		,		6		,	-ERROR_T	,	-ERROR_T	 }, /*0*/
/*1		>	*/	{ -GT_T		,	-GT_T		,	-GTE_T		,	-GT_T		,	-GT_T		,	-GT_T		,	-GT_T		,	-GT_T		,	-GT_T		,	-GT_T		,	-GT_T		,	-GT_T		,	-GT_T		,	-GT_T		,	-GT_T		,	-GT_T		,	-GT_T		,	-GT_T		,	-GT_T		,	-GT_T		,	-GT_T		,	-GT_T		,	-GT_T		 }, /*1*/
/*2		<	*/	{ -LT_T		,	-LT_T		,	-LTE_T		,	-LT_T		,	-LT_T		,	-LT_T		,	-LT_T		,	-LT_T		,	-LT_T		,	-LT_T		,	-LT_T		,	-LT_T		,	-LT_T		,	-LT_T		,	-LT_T		,	-LT_T		,	-LT_T		,	-LT_T		,	-LT_T		,	-LT_T		,	-LT_T		,	-LT_T		,	-LT_T		 }, /*2*/
/*3		"	*/	{	3		,		3		,		3		,		3		,		3		,		3		,		3		,		3		,	-STRLIT_T	,		3		,		3		,		3		,		3		,		3		,		3		,		3		,		3		,		3		,		3		,		3		,		3		,	-ERROR_T	,	-ERROR_T	 }, /*3*/
/*4		+	*/	{ -PLUS_T	,	-PLUS_T		,	-PLUS_T		,	-PLUS_T		,	-PLUS_T		,	-PLUS_T		,	-PLUS_T		,	-PLUS_T		,	-PLUS_T		,	-PLUS_T		,	-PLUS_T		,	-PLUS_T		,	-PLUS_T		,	-PLUS_T		,	-PLUS_T		,	-PLUS_T		,	-PLUS_T		,	-PLUS_T		,	-PLUS_T		,		7		,		6		,	-PLUS_T		,	-PLUS_T		 }, /*4*/
/*5		-	*/	{ -MINUS_T	,	-MINUS_T	,	-MINUS_T	,	-MINUS_T	,	-MINUS_T	,	-MINUS_T	,	-MINUS_T	,	-MINUS_T	,	-MINUS_T	,	-MINUS_T	,	-MINUS_T	,	-MINUS_T	,	-MINUS_T	,	-MINUS_T	,	-MINUS_T	,	-MINUS_T	,	-MINUS_T	,	-MINUS_T	,	-MINUS_T	,		7		,		6		,	-MINUS_T	,	-MINUS_T	 }, /*5*/
/*6	 number	*/	{ -NUMLIT_T	,	-NUMLIT_T	,	-NUMLIT_T	,	-NUMLIT_T	,	-NUMLIT_T	,	-NUMLIT_T	,	-NUMLIT_T	,	-NUMLIT_T	,	-NUMLIT_T	,	-NUMLIT_T	,	-NUMLIT_T	,	-NUMLIT_T	,	-NUMLIT_T	,	-NUMLIT_T	,	-NUMLIT_T	,	-NUMLIT_T	,	-NUMLIT_T	,	-NUMLIT_T	,	-NUMLIT_T	,		8		,		6		,	-NUMLIT_T	,	-NUMLIT_T	 }, /*6*/
/*7		.	*/	{ -ERROR_T	,	-ERROR_T	,	-ERROR_T	,	-ERROR_T	,	-ERROR_T	,	-ERROR_T	,	-ERROR_T	,	-ERROR_T	,	-ERROR_T	,	-ERROR_T	,	-ERROR_T	,	-ERROR_T	,	-ERROR_T	,	-ERROR_T	,	-ERROR_T	,	-ERROR_T	,	-ERROR_T	,	-ERROR_T	,	-ERROR_T	,	-ERROR_T	,		8		,	-ERROR_T	,	-ERROR_T	 }, /*7*/
/*8	.number	*/	{ -NUMLIT_T	,	-NUMLIT_T	,	-NUMLIT_T	,	-NUMLIT_T	,	-NUMLIT_T	,	-NUMLIT_T	,	-NUMLIT_T	,	-NUMLIT_T	,	-NUMLIT_T	,	-NUMLIT_T	,	-NUMLIT_T	,	-NUMLIT_T	,	-NUMLIT_T	,	-NUMLIT_T	,	-NUMLIT_T	,	-NUMLIT_T	,	-NUMLIT_T	,	-NUMLIT_T	,	-NUMLIT_T	,	-NUMLIT_T	,		8		,	-NUMLIT_T	,	-NUMLIT_T	 }, /*8*/
/*9		c	*/	{ -IDENT_T	,	-IDENT_T	,	-IDENT_T	,	-IDENT_T	,	-IDENT_T	,	-IDENT_T	,	-IDENT_T	,	-IDENT_T	,	-IDENT_T	,		12		,		10		,		10		,		12		,		12		,	-IDENT_T	,		12		,	-IDENT_T	,	-IDENT_T	,	-IDENT_T	,	-IDENT_T	,		12		,	-IDENT_T	,	-IDENT_T	 }, /*9*/
/*10   a/d	*/	{ -IDENT_T	,	-IDENT_T	,	-IDENT_T	,	-IDENT_T	,	-IDENT_T	,	-IDENT_T	,	-IDENT_T	,	-IDENT_T	,	-IDENT_T	,		12		,		12		,		10		,		11		,		12		,	-IDENT_T	,		12		,	-IDENT_T	,	-IDENT_T	,	-IDENT_T	,	-IDENT_T	,		12		,	-IDENT_T	,	-IDENT_T	 }, /*10*/
/*11	r	*/	{ -LISTOP_T	,	-LISTOP_T	,	-LISTOP_T	,	-LISTOP_T	,	-LISTOP_T	,	-LISTOP_T	,	-LISTOP_T	,	-LISTOP_T	,	-LISTOP_T	,		12		,		12		,		12		,		12		,		12		,	-LISTOP_T	,		12		,	-LISTOP_T	,	-LISTOP_T	,	-LISTOP_T	,	-LISTOP_T	,		12		,	-LISTOP_T	,	-LISTOP_T	 }, /*11*/
/*12  alpha	*/	{ -IDENT_T	,	-IDENT_T	,	-IDENT_T	,	-IDENT_T	,	-IDENT_T	,	-IDENT_T	,	-IDENT_T	,	-IDENT_T	,	-IDENT_T	,		12		,		12		,		12		,		12		,		12		,	-IDENT_T	,		12		,	-IDENT_T	,	-IDENT_T	,	-IDENT_T	,	-IDENT_T	,		12		,	-IDENT_T	,	-IDENT_T	 }  /*12*/
};



LexicalAnalyzer::LexicalAnalyzer (char * filename)
{
	// This function will initialize the lexical analyzer class
	input = ifstream(filename);

	line = "";
	linenum = 0;
	errors = 0;
	pos = 0;

	string f = filename;
	string outFilesName = f.substr(0, f.size() - 3);

	listingFile = ofstream(outFilesName + ".lst");
	tokenFile = ofstream(outFilesName + ".p1");
	debugFile = ofstream(outFilesName + ".dbg");

	ListingOutput("Input File: " + f + "\n");
}

LexicalAnalyzer::~LexicalAnalyzer ()
{
	// This function will complete the execution of the lexical analyzer class
	input.close();
	listingFile.close();
	tokenFile.close();
	debugFile.close();
}

token_type LexicalAnalyzer::GetToken ()
{
	// This function will find the next lexeme in the input file and return the token_type value associated with that lexeme

	// If we've reached the end of input and we've read the entire line,
	// return EOF_T.
	// Otherwise, try to get a new line.
	if (input.eof() == true && pos == line.length())
	{
		token = EOF_T;
		lexeme = "";
		return token;
	}
	else
	{
		tryGetNewLine();
	}

	token = NONE;
	lexeme = "";

	int current_state = 0;

	while (current_state >= 0 && pos < line.length())
	{
		// Get our new state based on the current state and current character
		current_state = strType(current_state, line[pos]);

		// Only add to the lexeme if we didn't end up back in the starting state
		if (current_state != 0)
		{
			lexeme += line[pos];
		}
		
		// If we've reached an accepting state, handle it
		if (current_state < 0)
		{
			token = (token_type)(current_state * -1);
			trySetToken();
		}

		pos += 1;
	}

	// Handle a case where we reached the end of the line but we
	// still have a token in the "buffer."
	if (pos == line.length() && current_state > 0)
	{
		// We want to force the newline state.
		current_state = strType(current_state, '\n');
		token = (token_type)(current_state * -1);
		DebugOutput("End of line lexeme: " + lexeme + "\n");
		trySetToken();
	}

	return token;
}

void LexicalAnalyzer::trySetToken()
{
	if (
		// Handle cases where we've read past the amount we needed
		// e.g. we read abc+ but we only want abc
		(find(begin(no_backup), end(no_backup), token) == end(no_backup)) &&
		// We also want to make sure we don't have a valid predicate
		(predicates.find(lexeme) == predicates.end()) &&
		pos != line.length()
		)
	{
		// Set the lexeme minus the extra character we added
		lexeme = lexeme.substr(0, lexeme.length() - 1);

		// Don't decrement pos if we're at the end of the line because
		// we rely on that to be able to get a new line or exit the program
		if (pos != line.length())
		{
			// Decrement pos so we reprocess the character we removed.
			pos--;
		}
	}

	// If we have an IDENT_T, then we need to see if it is a keyword or a predicate.
	if (token == IDENT_T)
	{
		if (lexeme.find('?') == string::npos)
		{
			// Question mark there is no question mark, see if it's a keyword.
			// Check keywords map to see if we find a matching keyword type.
			// If we don't, then we just have an IDENT_T.
			map<string, token_type>::iterator s = keywords.find(lexeme);
			if (s != keywords.end())
			{
				DebugOutput("Found keyword\n");
				token = s->second;
			}
		}
		else
		{
			// We have a question mark, so it may be a predicate.
			// Check the predicates map to see if we find a match.
			// If not, then we have an IDENT_T. We also need to decrement the
			// pos so that we process the ? as an ERROR_T.
			map<string, token_type>::iterator s = predicates.find(lexeme);
			if (s != predicates.end())
			{
				DebugOutput("Found predicate\n");
				token = s->second;
			}
		}
	}

	// Error reporting
	if (token == ERROR_T)
	{
		// +1 to pos so it's 1-indexed.
		ReportError("Error at " + to_string(linenum) + "," + to_string(pos + 1) + ": Invalid character found: " + line[pos]);
		ReportError("\n");
		errors++;
	}
}

void LexicalAnalyzer::tryGetNewLine()
{
	// Get a new line only if our current one is empty or
	// we've reached the end of the current line
	if (line.length() == 0 || pos == line.length())
	{
		DebugOutput("Getting new line\n");
		getline(input, line);
		linenum++;
		ListingOutput("\t" + to_string(linenum) + ": " + line + "\n");
		pos = 0;
	}
}

int LexicalAnalyzer::strType(int currentState, char c)
{
	// Special case for newlines
	if (c == '\n')
	{
		return dfa[currentState][NEWLINE_STATE];
	}
	// Special case for whitespace in general
	if (isspace(c))
	{
		return dfa[currentState][WHITESPACE_STATE];
	}
	// if c is not in our list of chars, do some other checks
	if (mp.count(c) == 0)
	{
		// Special case for if c is a digit
		if (isdigit(c))
		{
			return dfa[currentState][NUMBER_STATE];
		}
		// Special case for if c is an alpha (note that this
		// comes after the c/ad/r check)
		if (isalpha(c))
		{
			return dfa[currentState][ALPHA_STATE];
		}
	}
	// c is in our list of chars, give the state for that char
	else if (mp.count(c) > 0)
	{
		return dfa[currentState][mp[c]];
	}

	// Special case for if c is an unknown character (as in, it didn't
	// fulfill any of the previous categories)
	return dfa[currentState][UNKNOWN_STATE];
}

string LexicalAnalyzer::GetTokenName (token_type t) const
{
	// The GetTokenName function returns a string containing the name of the token passed to it. 
	return token_names[t];
}

string LexicalAnalyzer::GetLexeme () const
{
	// This function will return the lexeme found by the most recent call to  the get_token function

	return lexeme;
}

void LexicalAnalyzer::ReportError (const string & msg)
{
	// This function will be called to write an error message to a file
	ListingOutput(msg);
	DebugOutput(msg);
}

void LexicalAnalyzer::ListingOutput(const string & msg)
{
	listingFile << msg.c_str();
}

void LexicalAnalyzer::TokenOutput(const string & msg)
{
	tokenFile << msg.c_str();
}

void LexicalAnalyzer::DebugOutput(const string & msg)
{
	debugFile << msg.c_str();
}

int LexicalAnalyzer::NumErrors()
{
	return errors;
}
