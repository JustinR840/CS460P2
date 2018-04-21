import LexicalAnalyzer as LA
from Tokens import Token


class SyntacticalAnalyzer(object):

	# EOF_T, LPAREN_T, DEFINE_T, IDENT_T, RPAREN_T, NUMLIT_T, STRLIT_T, QUOTE_T, ELSE_T, IF_T, COND_T, LISTOP_T, CONDS_T, AND_T, OR_T, NOT_T, NUMBERP_T, SYMBOLP_T, LISTP_T, ZEROP_T, NULLP_T, STRINGP_T, PLUS_T, MINUS_T, DIV_T, MULT_T, MODULO_T, EQUALTO_T, GT_T, LT_T, GTE_T, LTE_T, IDENT_T, DISPLAY_T, NEWLINE_T

	firsts = [
		[],
		[],
		[],
		[],
		[],
		[],
		[],
		[],
		[],
		[],
		[],
		[],
		[],
		[]
	]
	follows = [[],[],[]]




	def __init__(self, filename):
		self.filename = filename
		self.p2File = open(self.filename[:-3] + ".p2", "a")
		self.ct = ""
		self.lex = LA.LexicalAnalyzer(filename.encode("utf-8"))

	def __del__(self):
		self.p2File.close()

	def ReportError(self, err):
		self.writeToP2ListingFile(err)

	def doHeaderOutput(self, funcName):
		self.writeToP2ListingFile("Entering " + funcName + " function; current token is: " + self.lex.getTokenName(self.ct) + ", lexeme: " + self.lex.getLexeme())

	def doExitOutput(self, funcName):
		self.writeToP2ListingFile("Exiting " + funcName + " function; current token is: " + self.lex.getTokenName(self.ct) + ", lexeme: " + self.lex.getLexeme())

	def doRuleOutput(self, rule):
		self.writeToP2ListingFile("Using Rule: " + rule)

	def writeToP2ListingFile(self, text):
		self.p2File.write(text + "\n")


	# TODO: Declare the first/follows outside of their function calls (make static) (table maybe?)


	def parse(self):
		# Get the first token and start the program!
		self.ct = self.lex.getToken()
		errors = self.program()
		print(errors, "found in Syntactical Analysis.")

	def program(self):
		self.doHeaderOutput("Program")

		firsts = [Token.LPAREN_T]
		follows = []

		errors = 0

		self.doRuleOutput("2")
		errors += self.define()
		self.doRuleOutput("3")
		errors += self.more_defines()

		if (self.ct == Token.EOF_T):
			pass
		# self.ct = self.lex.getToken()
		else:
			errors += 1
			self.ReportError("Program: Unexpected " + self.lex.getTokenName(self.ct) + "; Expected EOF_T")

		self.doExitOutput("Program")
		return errors

	def define(self):
		self.doHeaderOutput("Define")

		firsts = [Token.LPAREN_T]
		follows = [Token.EOF_T, Token.LPAREN_T]

		errors = 0

		# Cascading if statements because we need to fulfill ALL requirements to be valid

		if (self.ct == Token.LPAREN_T):
			self.ct = self.lex.getToken()

			if (self.ct == Token.DEFINE_T):
				self.ct = self.lex.getToken()

				if (self.ct == Token.LPAREN_T):
					self.ct = self.lex.getToken()

					if (self.ct == Token.IDENT_T):
						self.ct = self.lex.getToken()

						self.doRuleOutput("16-17")
						errors += self.param_list()

						if (self.ct == Token.RPAREN_T):
							self.ct = self.lex.getToken()

							self.doRuleOutput("7-9")
							errors += self.stmt()
							self.doRuleOutput("5-6")
							errors += self.stmt_list()

							if (self.ct == Token.RPAREN_T):
								self.ct = self.lex.getToken()
							else:
								errors += 1
								self.ReportError("Define: Unexpected " + self.lex.getTokenName(self.ct) + "; Expected RPAREN_T")
						else:
							errors += 1
							self.ReportError("Define: Unexpected " + self.lex.getTokenName(self.ct) + "; Expected RPAREN_T")
					else:
						errors += 1
						self.ReportError("Define: Unexpected " + self.lex.getTokenName(self.ct) + "; Expected IDENT_T")
				else:
					errors += 1
					self.ReportError("Define: Unexpected " + self.lex.getTokenName(self.ct) + "; Expected LPAREN_T")
			else:
				errors += 1
				self.ReportError("Define: Unexpected " + self.lex.getTokenName(self.ct) + "; Expected DEFINE_T")
		else:
			errors += 1
			self.ReportError("Define: Unexpected " + self.lex.getTokenName(self.ct) + "; Expected LPAREN_T")

		self.doExitOutput("Define")
		return errors


	def more_defines(self):
		self.doHeaderOutput("More_Defines")

		firsts = [Token.EOF_T, Token.LPAREN_T]
		follows = [Token.EOF_T]

		errors = 0

		if (self.ct not in follows):
			self.doRuleOutput("3")
			errors += self.define()
			errors += self.more_defines()
		else:
			self.doRuleOutput("4")

		self.doExitOutput("More_Defines")
		return errors


	def stmt_list(self):
		self.doHeaderOutput("Stmt_List")

		firsts = [Token.RPAREN_T, Token.NUMLIT_T, Token.STRLIT_T, Token.QUOTE_T, Token.IDENT_T,
		          Token.LPAREN_T]
		follows = [Token.RPAREN_T]

		errors = 0

		if (self.ct not in follows):
			self.doRuleOutput("5")
			errors += self.stmt()
			errors += self.stmt_list()
		else:
			self.doRuleOutput("6")

		self.doExitOutput("Stmt_List")
		return errors


	def stmt(self):
		self.doHeaderOutput("Stmt")

		firsts = [Token.IDENT_T, Token.LPAREN_T, Token.NUMLIT_T, Token.STRLIT_T, Token.QUOTE_T]
		follows = [Token.RPAREN_T, Token.IDENT_T, Token.LPAREN_T, Token.NUMLIT_T, Token. STRLIT_T, Token.QUOTE_T]

		errors = 0

		if (self.ct == Token.IDENT_T):
			self.doRuleOutput("8")
			self.ct = self.lex.getToken()
		elif (self.ct == Token.LPAREN_T):
			self.doRuleOutput("9")
			self.ct = self.lex.getToken()

			errors += self.action()
			if (self.ct == Token.RPAREN_T):
				self.ct = self.lex.getToken()
			else:
				errors += 1
				self.ReportError("Stmt: Unexpected " + self.lex.getTokenName(self.ct) + "; Expected RPAREN_T")
		else:
			self.doRuleOutput("7")
			errors += self.literal()

		self.doExitOutput("Stmt")
		return errors


	def literal(self):
		self.doHeaderOutput("Literal")

		firsts = [Token.NUMLIT_T, Token.STRLIT_T, Token.QUOTE_T]
		follows = [Token.RPAREN_T, Token.IDENT_T, Token.LPAREN_T, Token.NUMLIT_T, Token. STRLIT_T, Token.QUOTE_T]

		errors = 0

		if (self.ct == Token.NUMLIT_T or self.ct == Token.STRLIT_T):
			self.doRuleOutput("10 or 11")
			self.ct = self.lex.getToken()
		elif (self.ct == Token.QUOTE_T):
			self.doRuleOutput("12")
			self.ct = self.lex.getToken()
			errors += self.quoted_lit()

		self.doExitOutput("Literal")
		return errors


	def quoted_lit(self):
		self.doHeaderOutput("Quoted_Lit")

		firsts = [Token.LPAREN_T, Token.IDENT_T, Token.NUMLIT_T, Token.STRLIT_T, Token.CONS_T, Token.IF_T, Token.DISPLAY_T, Token.NEWLINE_T, Token.LISTOP_T, Token.AND_T, Token.OR_T, Token.NOT_T, Token.DEFINE_T, Token.NUMBERP_T, Token.SYMBOLP_T, Token.LISTP_T, Token.ZEROP_T, Token.NULLP_T, Token.STRINGP_T, Token.PLUS_T, Token.MINUS_T, Token.DIV_T, Token.MULT_T, Token.MODULO_T, Token.EQUALTO_T, Token.GT_T, Token.LT_T, Token.GTE_T, Token.LTE_T, Token.QUOTE_T, Token.COND_T, Token.ELSE_T]
		follows = [Token.RPAREN_T, Token.IDENT_T, Token.LPAREN_T, Token.NUMLIT_T, Token. STRLIT_T, Token.QUOTE_T]

		errors = 0

		self.doRuleOutput("13")
		errors += self.any_other_token()

		self.doExitOutput("Quoted_Lit")
		return errors


	def more_tokens(self):
		self.doHeaderOutput("More_Tokens")

		firsts = [Token.RPAREN_T, Token.LPAREN_T, Token.IDENT_T, Token.NUMLIT_T, Token.STRLIT_T, Token.CONS_T, Token.IF_T, Token.DISPLAY_T, Token.NEWLINE_T, Token.LISTOP_T, Token.AND_T, Token.OR_T, Token.NOT_T, Token.DEFINE_T, Token.NUMBERP_T, Token.SYMBOLP_T, Token.LISTP_T, Token.ZEROP_T, Token.NULLP_T, Token.STRINGP_T, Token.PLUS_T, Token.MINUS_T, Token.DIV_T, Token.MULT_T, Token.MODULO_T, Token.EQUALTO_T, Token.GT_T, Token.LT_T, Token.GTE_T, Token.LTE_T, Token.QUOTE_T, Token.COND_T, Token.ELSE_T]
		follows = [Token.RPAREN_T]

		errors = 0


		if (self.ct not in follows):
			self.doRuleOutput("14")
			errors += self.any_other_token()
			errors += self.more_tokens()
		else:
			self.doRuleOutput("15")

		self.doExitOutput("More_Tokens")
		return errors


	def param_list(self):
		self.doHeaderOutput("Param_List")

		firsts = [Token.IDENT_T, Token.RPAREN_T]
		follows = [Token.RPAREN_T]

		errors = 0

		if (self.ct == Token.IDENT_T):
			self.doRuleOutput("16")
			self.ct = self.lex.getToken()
			errors += self.param_list()
		else:
			self.doRuleOutput("17")

		self.doExitOutput("Param_List")
		return errors


	def else_part(self):
		self.doHeaderOutput("Else_Part")

		firsts = [Token.RPAREN_T, Token.IDENT_T, Token.LPAREN_T, Token.NUMLIT_T, Token.STRLIT_T, Token.QUOTE_T]
		follows = [Token.RPAREN_T]

		errors = 0

		if (self.ct not in follows):
			self.doRuleOutput("18")
			errors += self.stmt()
		else:
			self.doRuleOutput("19")

		self.doExitOutput("Else_Part")
		return errors


	def stmt_pair(self):
		self.doHeaderOutput("Stmt_Pair")

		firsts = [Token.LPAREN_T, Token.RPAREN_T]
		follows = [Token.RPAREN_T]

		errors = 0

		if (self.ct == Token.LPAREN_T):
			self.doRuleOutput("20")
			self.ct = self.lex.getToken()
			errors += self.stmt_pair_body()
		else:
			self.doRuleOutput("21")

		self.doExitOutput("Stmt_Pair")
		return errors


	def stmt_pair_body(self):
		self.doHeaderOutput("Stmt_Pair_Body")

		firsts = [Token.ELSE_T, Token.IDENT_T, Token.LPAREN_T, Token.NUMLIT_T, Token.STRLIT_T, Token.QUOTE_T]
		follows = [Token.RPAREN_T]

		errors = 0

		if (self.ct == Token.ELSE_T):
			self.doRuleOutput("23")
			self.ct = self.lex.getToken()
			errors += self.stmt()
			if (self.ct == Token.RPAREN_T):
				self.ct = self.lex.getToken()
			else:
				errors += 1
				self.ReportError("Stmt_Pair_Body: Unexpected " + self.lex.getTokenName(self.ct) + "; Expected RPAREN_T")
		else:
			self.doRuleOutput("22")
			errors += self.stmt()
			errors += self.stmt()
			if (self.ct == Token.RPAREN_T):
				self.ct = self.lex.getToken()
				errors += self.stmt_pair()
			else:
				errors += 1
				self.ReportError("Stmt_Pair_Body: Unexpected " + self.lex.getTokenName(self.ct) + "; Expected RPAREN_T")

		self.doExitOutput("Stmt_Pair_Body")
		return errors


	def action(self):
		self.doHeaderOutput("Action")

		firsts = [Token.IF_T, Token.COND_T, Token.LISTOP_T, Token.CONS_T, Token.AND_T, Token.OR_T, Token.NOT_T, Token.NUMBERP_T, Token.SYMBOLP_T, Token.LISTP_T, Token.ZEROP_T, Token.NULLP_T, Token.STRINGP_T, Token.PLUS_T, Token.MINUS_T, Token.DIV_T, Token.MULT_T, Token.MODULO_T, Token.EQUALTO_T, Token.GT_T, Token.LT_T, Token.GTE_T, Token.LTE_T, Token.IDENT_T, Token.DISPLAY_T, Token.NEWLINE_T]
		follows = [Token.RPAREN_T]

		errors = 0

		if (self.ct == Token.IF_T):
			self.doRuleOutput("24")
			self.ct = self.lex.getToken()
			errors += self.stmt()
			errors += self.stmt()
			errors += self.else_part()
		elif (self.ct == Token.COND_T):
			self.doRuleOutput("25")
			self.ct = self.lex.getToken()
			if (self.ct == Token.LPAREN_T):
				self.ct = self.lex.getToken()
				errors += self.stmt_pair_body()
			else:
				errors += 1
				self.ReportError("Action: Unexpected " + self.lex.getTokenName(self.ct) + "; Expected LPAREN_T")
		elif (self.ct == Token.LISTOP_T or self.ct == Token.NOT_T or
				      self.ct == Token.NUMBERP_T or self.ct == Token.SYMBOLP_T or
				      self.ct == Token.LISTP_T or self.ct == Token.ZEROP_T or
				      self.ct == Token.NULLP_T or self.ct == Token.NULLP_T or
				      self.ct == Token.STRINGP_T or self.ct == Token.DISPLAY_T):
			self.doRuleOutput("26 or 30 or 31 or 32 or 33 or 34 or 35 or 36 or 48")
			self.ct = self.lex.getToken()
			errors += self.stmt()
		elif (self.ct == Token.AND_T or self.ct == Token.OR_T or
				      self.ct == Token.PLUS_T or self.ct == Token.MULT_T or
				      self.ct == Token.EQUALTO_T or self.ct == Token.GT_T or
				      self.ct == Token.LT_T or self.ct == Token.GTE_T or
				      self.ct == Token.LTE_T or self.ct == Token.IDENT_T):
			self.doRuleOutput("28 or 29 or 37 or 40 or 42 or 43 or 45 or 46 or 47")
			self.ct = self.lex.getToken()
			errors += self.stmt_list()
		elif (self.ct == Token.CONS_T or self.ct == Token.MODULO_T):
			self.doRuleOutput("27 or 41")
			self.ct = self.lex.getToken()
			errors += self.stmt()
			errors += self.stmt()
		elif (self.ct == Token.MINUS_T or self.ct == Token.DIV_T):
			self.doRuleOutput("38 or 39")
			self.ct = self.lex.getToken()
			errors += self.stmt()
			errors += self.stmt_list()
		elif (self.ct == Token.NEWLINE_T):
			self.doRuleOutput("49")
			self.ct = self.lex.getToken()
		else:
			errors += 1
			self.ReportError("Action: Unexpected " + self.lex.getTokenName(self.ct) + "; <action> expected")

		self.doExitOutput("Action")
		return errors


	def any_other_token(self):
		self.doHeaderOutput("Any_Other_Token")

		firsts = [Token.LPAREN_T, Token.IDENT_T, Token.NUMLIT_T, Token.STRLIT_T, Token.CONS_T, Token.IF_T, Token.DISPLAY_T, Token.NEWLINE_T, Token.LISTOP_T, Token.AND_T, Token.OR_T, Token.NOT_T, Token.DEFINE_T, Token.NUMBERP_T, Token.SYMBOLP_T, Token.LISTP_T, Token.ZEROP_T, Token.NULLP_T, Token.STRINGP_T, Token.PLUS_T, Token.MINUS_T, Token.DIV_T, Token.MULT_T, Token.MODULO_T, Token.EQUALTO_T, Token.GT_T, Token.LT_T, Token.GTE_T, Token.LTE_T, Token.QUOTE_T, Token.COND_T, Token.ELSE_T]

		follows = [Token.RPAREN_T, Token.LPAREN_T, Token.IDENT_T, Token.NUMLIT_T, Token.STRLIT_T, Token.CONS_T, Token.IF_T, Token.DISPLAY_T, Token.NEWLINE_T, Token.LISTOP_T, Token.AND_T, Token.OR_T, Token.NOT_T, Token.DEFINE_T, Token.NUMBERP_T, Token.SYMBOLP_T, Token.LISTP_T, Token.ZEROP_T, Token.NULLP_T, Token.STRINGP_T, Token.PLUS_T, Token.MINUS_T, Token.DIV_T, Token.MULT_T, Token.MODULO_T, Token.EQUALTO_T, Token.GT_T, Token.LT_T, Token.GTE_T, Token.LTE_T, Token.QUOTE_T, Token.COND_T, Token.ELSE_T]

		errors = 0

		if (self.ct == Token.LPAREN_T):
			self.doRuleOutput("50")
			self.ct = self.lex.getToken()
			errors += self.more_tokens()
			if (self.ct == Token.RPAREN_T):
				self.ct = self.lex.getToken()
			else:
				errors += 1
				self.ReportError("Any_Other_Token: Unexpected " + self.lex.getTokenName(self.ct) + "; Expected RPAREN_T")
		elif (self.ct == Token.QUOTE_T):
			self.doRuleOutput("79")
			self.ct = self.lex.getToken()
			errors += self.any_other_token()
		elif (self.ct == Token.IDENT_T or self.ct == Token.NUMLIT_T or
				      self.ct == Token.STRLIT_T or self.ct == Token.CONS_T or
				      self.ct == Token.IF_T or self.ct == Token.DISPLAY_T or
				      self.ct == Token.NEWLINE_T or self.ct == Token.LISTOP_T or
				      self.ct == Token.AND_T or self.ct == Token.OR_T or
				      self.ct == Token.NOT_T or self.ct == Token.DEFINE_T or
				      self.ct == Token.NUMBERP_T or self.ct == Token.SYMBOLP_T or
				      self.ct == Token.LISTP_T or self.ct == Token.ZEROP_T or
				      self.ct == Token.NULLP_T or self.ct == Token.STRINGP_T or
				      self.ct == Token.PLUS_T or self.ct == Token.MINUS_T or
				      self.ct == Token.DIV_T or self.ct == Token.MULT_T or
				      self.ct == Token.MODULO_T or self.ct == Token.EQUALTO_T or
				      self.ct == Token.GT_T or self.ct == Token.LT_T or
				      self.ct == Token.GTE_T or self.ct == Token.LTE_T or
				      self.ct == Token.COND_T or self.ct == Token.ELSE_T):
			self.doRuleOutput("Somewhere Between 51 - 81, excluding 79")
			self.ct = self.lex.getToken()
		else:
			errors += 1
			self.ReportError("Any_Other_Token: Unexpected " + self.lex.getTokenName(self.ct) + "; Expected <any_other_token>")

		self.doExitOutput("Any_Other_Token")
		return errors
