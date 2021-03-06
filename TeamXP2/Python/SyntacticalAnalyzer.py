import LexicalAnalyzer as LA
from Enums import Token, Rule
import Helpers


class SyntacticalAnalyzer(object):
	def __init__(self, filename):
		self.filename = filename
		self.p2File = open(self.filename[:-3] + ".p2", "a")
		self.ct = ""
		self.lex = LA.LexicalAnalyzer(filename.encode("utf-8"))

		self.rule_mappings = {
			1: self.program,
			2: self.define,
			3: self.more_defines,
			4: self.stmt_list,
			5: self.stmt,
			6: self.literal,
			7: self.quoted_lit,
			8: self.more_tokens,
			9: self.param_list,
			10: self.else_part,
			11: self.stmt_pair,
			12: self.stmt_pair_body,
			13: self.action,
			14: self.any_other_token
		}

	def __del__(self):
		self.p2File.close()

	def ReportError(self, err):
		self.writeToP2ListingFile(err)

	def doHeaderOutput(self, funcName):
		self.writeToP2ListingFile("Entering " + funcName + " function; current token is: " + self.lex.getTokenName(self.ct) + ", lexeme: " + self.lex.getLexeme())

	def doExitOutput(self, funcName):
		self.writeToP2ListingFile("Exiting " + funcName + " function; current token is: " + self.lex.getTokenName(self.ct))

	def doRuleOutput(self, rule):
		self.writeToP2ListingFile("Using Rule " + rule)

	def writeToP2ListingFile(self, text):
		self.p2File.write(text + "\n")

	def getRuleToUse(self, prod_rule):
		if(prod_rule <= 81):
			if(prod_rule >= 50):
				return Rule.ANY_OTHER_TOKEN
			elif(prod_rule >= 24):
				return Rule.ACTION
			elif(prod_rule >= 22):
				return Rule.STMT_PAIR_BODY
			elif(prod_rule >= 20):
				return Rule.STMT_PAIR
			elif(prod_rule >= 18):
				return Rule.ELSE_PART
			elif(prod_rule >= 16):
				return Rule.PARAM_LIST
			elif(prod_rule >= 14):
				return Rule.MORE_TOKENS
			elif(prod_rule >= 13):
				return Rule.QUOTED_LIT
			elif(prod_rule >= 10):
				return Rule.LITERAL
			elif(prod_rule >= 7):
				return Rule.STMT
			elif(prod_rule >= 5):
				return Rule.STMT_LIST
			elif(prod_rule >= 3):
				return Rule.MORE_DEFINES
			elif(prod_rule >= 2):
				return Rule.DEFINE
			elif(prod_rule >= 1):
				return Rule.PROGRAM

	def parse(self):
		# Get the first token and start the program!
		self.ct = self.lex.getToken()
		self.doRuleOutput("1")
		errors = self.program()
		print(errors, "found in Syntactical Analysis.")

	def program(self):
		self.doHeaderOutput("Program")
		CURRENT_RULE = Rule.PROGRAM
		errors = 0

		while (Helpers.firsts[CURRENT_RULE][self.ct] == 0 and Helpers.follows[CURRENT_RULE][self.ct] == 0):
			self.ReportError("Unexpected token: '" + str(self.ct) + "'")
			self.ct = self.lex.getToken()
			errors += 1

		self.doRuleOutput("2")
		errors += self.define()
		self.doRuleOutput("3")
		errors += self.more_defines()

		if (self.ct == Token.EOF_T):
			pass
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

						errors += self.param_list()

						if (self.ct == Token.RPAREN_T):
							self.ct = self.lex.getToken()

							errors += self.stmt()
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
			self.ct = self.lex.getToken()
			errors += 1

		if(Helpers.follows[CURRENT_RULE][self.ct] == 0):
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
			self.ct = self.lex.getToken()
			errors += 1

		if (Helpers.follows[CURRENT_RULE][self.ct] == 0):
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
			self.ct = self.lex.getToken()
			errors += 1

		if (self.ct == Token.NUMLIT_T or self.ct == Token.STRLIT_T):
			rule_num = Helpers.rule_transitions[CURRENT_RULE][self.ct]
			self.doRuleOutput(str(rule_num))
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
			self.ct = self.lex.getToken()
			errors += 1

		if(Helpers.follows[CURRENT_RULE][self.ct] == 0):
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
			self.ct = self.lex.getToken()
			errors += 1

		if(Helpers.follows[CURRENT_RULE][self.ct] == 0):
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
		else:
			rule_num = Helpers.rule_transitions[CURRENT_RULE][self.ct]
			if(rule_num != 0):
				self.doRuleOutput(str(rule_num))
				if (self.ct == Token.LISTOP_T or self.ct == Token.NOT_T or
						      self.ct == Token.NUMBERP_T or self.ct == Token.SYMBOLP_T or
						      self.ct == Token.LISTP_T or self.ct == Token.ZEROP_T or
						      self.ct == Token.NULLP_T or self.ct == Token.NULLP_T or
						      self.ct == Token.STRINGP_T or self.ct == Token.DISPLAY_T):
					self.ct = self.lex.getToken()
					errors += self.stmt()
				elif (self.ct == Token.AND_T or self.ct == Token.OR_T or
						      self.ct == Token.PLUS_T or self.ct == Token.MULT_T or
						      self.ct == Token.EQUALTO_T or self.ct == Token.GT_T or
						      self.ct == Token.LT_T or self.ct == Token.GTE_T or
						      self.ct == Token.LTE_T or self.ct == Token.IDENT_T):
					self.ct = self.lex.getToken()
					errors += self.stmt_list()
				elif (self.ct == Token.CONS_T or self.ct == Token.MODULO_T):
					self.ct = self.lex.getToken()
					errors += self.stmt()
					errors += self.stmt()
				elif (self.ct == Token.MINUS_T or self.ct == Token.DIV_T):
					self.ct = self.lex.getToken()
					errors += self.stmt()
					errors += self.stmt_list()
				elif (self.ct == Token.NEWLINE_T):
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
			self.ct = self.lex.getToken()
			errors += 1

		if(self.ct == Token.LPAREN_T):
			self.doRuleOutput("50")
			self.ct = self.lex.getToken()
			errors += self.more_tokens()
			if(self.ct == Token.RPAREN_T):
				self.ct = self.lex.getToken()
			else:
				errors += 1
				self.ReportError("Any_Other_Token: Unexpected " + self.lex.getTokenName(self.ct) + "; Expected RPAREN_T")
		elif (self.ct == Token.QUOTE_T):
			self.doRuleOutput("79")
			self.ct = self.lex.getToken()
			errors += self.any_other_token()
		else:
			rule_num = Helpers.rule_transitions[CURRENT_RULE][self.ct]
			if(rule_num != 0):
				self.doRuleOutput(str(rule_num))
				rule_to_use = self.getRuleToUse(rule_num)
				self.rule_mappings[rule_to_use]()
			else:
				errors += 1
				self.ReportError("Any_Other_Token: Unexpected " + self.lex.getTokenName(self.ct) + "; Expected <any_other_token>")

		self.doExitOutput("Any_Other_Token")
		return errors