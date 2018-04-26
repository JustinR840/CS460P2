import LexicalAnalyzer as LA
from Enums import Token, Rule
import Helpers


class SyntacticalAnalyzer(object):





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


	def parse(self):
		# Get the first token and start the program!
		self.ct = self.lex.getToken()
		errors = self.program()
		print(errors, "found in Syntactical Analysis.")

	def program(self):
		self.doHeaderOutput("Program")
		CURRENT_RULE = Rule.PROGRAM
		errors = 0

		while (Helpers.firsts[CURRENT_RULE][self.ct] == 0 and Helpers.follows[CURRENT_RULE][self.ct] == 0):
			self.ReportError("Unexpected token: '" + str(self.ct) + "'")
			print("Unexpected token: '" + str(self.ct) + "'")
			self.ct = self.lex.getToken()
			errors += 1

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
		CURRENT_RULE = Rule.DEFINE
		errors = 0

		while (Helpers.firsts[CURRENT_RULE][self.ct] == 0 and Helpers.follows[CURRENT_RULE][self.ct] == 0):
			self.ReportError("Unexpected token: '" + str(self.ct) + "'")
			print("Unexpected token: '" + str(self.ct) + "'")
			self.ct = self.lex.getToken()
			errors += 1

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
		CURRENT_RULE = Rule.MORE_DEFINES
		errors = 0

		while (Helpers.firsts[CURRENT_RULE][self.ct] == 0 and Helpers.follows[CURRENT_RULE][self.ct] == 0):
			self.ReportError("Unexpected token: '" + str(self.ct) + "'")
			print("Unexpected token: '" + str(self.ct) + "'")
			self.ct = self.lex.getToken()
			errors += 1

		if(Helpers.follows[CURRENT_RULE][self.ct] == 0):
		#if (self.ct not in follows):
			self.doRuleOutput("3")
			errors += self.define()
			errors += self.more_defines()
		else:
			self.doRuleOutput("4")

		self.doExitOutput("More_Defines")
		return errors


	def stmt_list(self):
		self.doHeaderOutput("Stmt_List")
		CURRENT_RULE = Rule.STMT_LIST
		errors = 0

		while (Helpers.firsts[CURRENT_RULE][self.ct] == 0 and Helpers.follows[CURRENT_RULE][self.ct] == 0):
			self.ReportError("Unexpected token: '" + str(self.ct) + "'")
			print("Unexpected token: '" + str(self.ct) + "'")
			self.ct = self.lex.getToken()
			errors += 1

		if (Helpers.follows[CURRENT_RULE][self.ct] == 0):
		#if (self.ct not in follows):
			self.doRuleOutput("5")
			errors += self.stmt()
			errors += self.stmt_list()
		else:
			self.doRuleOutput("6")

		self.doExitOutput("Stmt_List")
		return errors


	def stmt(self):
		self.doHeaderOutput("Stmt")
		CURRENT_RULE = Rule.STMT
		errors = 0

		while (Helpers.firsts[CURRENT_RULE][self.ct] == 0 and Helpers.follows[CURRENT_RULE][self.ct] == 0):
			self.ReportError("Unexpected token: '" + str(self.ct) + "'")
			print("Unexpected token: '" + str(self.ct) + "'")
			self.ct = self.lex.getToken()
			errors += 1

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
		CURRENT_RULE = Rule.LITERAL
		errors = 0

		while (Helpers.firsts[CURRENT_RULE][self.ct] == 0 and Helpers.follows[CURRENT_RULE][self.ct] == 0):
			self.ReportError("Unexpected token: '" + str(self.ct) + "'")
			print("Unexpected token: '" + str(self.ct) + "'")
			self.ct = self.lex.getToken()
			errors += 1

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
		CURRENT_RULE = Rule.QUOTED_LIT
		errors = 0

		while (Helpers.firsts[CURRENT_RULE][self.ct] == 0 and Helpers.follows[CURRENT_RULE][self.ct] == 0):
			self.ReportError("Unexpected token: '" + str(self.ct) + "'")
			print("Unexpected token: '" + str(self.ct) + "'")
			self.ct = self.lex.getToken()
			errors += 1

		self.doRuleOutput("13")
		errors += self.any_other_token()

		self.doExitOutput("Quoted_Lit")
		return errors


	def more_tokens(self):
		self.doHeaderOutput("More_Tokens")
		CURRENT_RULE = Rule.MORE_TOKENS
		errors = 0

		while (Helpers.firsts[CURRENT_RULE][self.ct] == 0 and Helpers.follows[CURRENT_RULE][self.ct] == 0):
			self.ReportError("Unexpected token: '" + str(self.ct) + "'")
			print("Unexpected token: '" + str(self.ct) + "'")
			self.ct = self.lex.getToken()
			errors += 1

		if(Helpers.follows[CURRENT_RULE][self.ct] == 0):
		#if (self.ct not in follows):
			self.doRuleOutput("14")
			errors += self.any_other_token()
			errors += self.more_tokens()
		else:
			self.doRuleOutput("15")

		self.doExitOutput("More_Tokens")
		return errors


	def param_list(self):
		self.doHeaderOutput("Param_List")
		CURRENT_RULE = Rule.PARAM_LIST
		errors = 0

		while (Helpers.firsts[CURRENT_RULE][self.ct] == 0 and Helpers.follows[CURRENT_RULE][self.ct] == 0):
			self.ReportError("Unexpected token: '" + str(self.ct) + "'")
			print("Unexpected token: '" + str(self.ct) + "'")
			self.ct = self.lex.getToken()
			errors += 1

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
		CURRENT_RULE = Rule.ELSE_PART
		errors = 0

		while (Helpers.firsts[CURRENT_RULE][self.ct] == 0 and Helpers.follows[CURRENT_RULE][self.ct] == 0):
			self.ReportError("Unexpected token: '" + str(self.ct) + "'")
			print("Unexpected token: '" + str(self.ct) + "'")
			self.ct = self.lex.getToken()
			errors += 1

		if(Helpers.follows[CURRENT_RULE][self.ct] == 0):
		#if (self.ct not in follows):
			self.doRuleOutput("18")
			errors += self.stmt()
		else:
			self.doRuleOutput("19")

		self.doExitOutput("Else_Part")
		return errors


	def stmt_pair(self):
		self.doHeaderOutput("Stmt_Pair")
		CURRENT_RULE = Rule.STMT_PAIR
		errors = 0

		while (Helpers.firsts[CURRENT_RULE][self.ct] == 0 and Helpers.follows[CURRENT_RULE][self.ct] == 0):
			self.ReportError("Unexpected token: '" + str(self.ct) + "'")
			print("Unexpected token: '" + str(self.ct) + "'")
			self.ct = self.lex.getToken()
			errors += 1

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
		CURRENT_RULE = Rule.STMT_PAIR_BODY
		errors = 0

		while (Helpers.firsts[CURRENT_RULE][self.ct] == 0 and Helpers.follows[CURRENT_RULE][self.ct] == 0):
			self.ReportError("Unexpected token: '" + str(self.ct) + "'")
			print("Unexpected token: '" + str(self.ct) + "'")
			self.ct = self.lex.getToken()
			errors += 1

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
		CURRENT_RULE = Rule.ACTION
		errors = 0

		while (Helpers.firsts[CURRENT_RULE][self.ct] == 0 and Helpers.follows[CURRENT_RULE][self.ct] == 0):
			self.ReportError("Unexpected token: '" + str(self.ct) + "'")
			print("Unexpected token: '" + str(self.ct) + "'")
			self.ct = self.lex.getToken()
			errors += 1

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
		CURRENT_RULE = Rule.ANY_OTHER_TOKEN
		errors = 0

		while (Helpers.firsts[CURRENT_RULE][self.ct] == 0 and Helpers.follows[CURRENT_RULE][self.ct] == 0):
			self.ReportError("Unexpected token: '" + str(self.ct) + "'")
			print("Unexpected token: '" + str(self.ct) + "'")
			self.ct = self.lex.getToken()
			errors += 1

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

