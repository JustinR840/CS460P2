from Tokens import Token

class SyntacticalAnalyzer(object):
	def __init__(self, lex):
		self.ct = ""
		self.lex = lex


	def ReportError(self, err):
		print(err)
		# TODO: Error reporting for the Syntactical Analyzer

	# TODO: Other output forms for Syntactical Analyzer


	def parse(self):
		# Do other stuff here like make output files maybe
		self.ct = self.lex.getToken()
		errors = self.program()
		print(errors, "found in Syntactical Analysis.")


	def program(self):
		firsts = [Token.LPAREN_T]
		follows = []

		errors = 0

		errors += self.define()
		errors += self.more_defines()

		if(self.ct == Token.EOF_T):
			pass
			# self.ct = self.lex.getToken()
		else:
			errors += 1
			self.ReportError("Program: Expected EOF_T")

		return errors


	def define(self):
		firsts = [Token.LPAREN_T]
		follows = [Token.EOF_T, Token.LPAREN_T]

		errors = 0

		if(self.ct == Token.LPAREN_T):
			self.ct = self.lex.getToken()
		else:
			errors += 1
			self.ReportError("Define: Expected LPAREN_T")

		if(self.ct == Token.DEFINE_T):
			self.ct = self.lex.getToken()
		else:
			errors += 1
			self.ReportError("Define: Expected DEFINE_T")

		if(self.ct == Token.LPAREN_T):
			self.ct = self.lex.getToken()
		else:
			errors += 1
			self.ReportError("Define: Expected LPAREN_T")

		if(self.ct == Token.IDENT_T):
			self.ct = self.lex.getToken()
		else:
			errors += 1
			self.ReportError("Define: Expected IDENT_T")

		errors += self.param_list()

		if(self.ct == Token.RPAREN_T):
			self.ct = self.lex.getToken()
		else:
			errors += 1
			self.ReportError("Define: Expected RPAREN_T")

		errors += self.stmt()
		errors += self.stmt_list()

		if(self.ct == Token.RPAREN_T):
			self.ct = self.lex.getToken()
		else:
			errors += 1
			self.ReportError("Define: Expected RPAREN_T")

		return errors


	def more_defines(self):
		firsts = []
		follows = []

		errors = 0

		errors += self.define()
		errors += self.more_defines()

		return errors


	def stmt_list(self):
		firsts = []
		follows = []

		errors = 0

		errors += self.stmt()
		errors += self.stmt_list()

		return errors


	def stmt(self):
		firsts = []
		follows = []

		errors = 0

		if(self.ct == Token.IDENT_T):
			self.ct = self.lex.getToken()
		elif(self.ct == Token.LPAREN_T):
			self.ct = self.lex.getToken()
			errors += self.action()
			if(self.ct == Token.RPAREN_T):
				self.ct = self.lex.getToken()
			else:
				errors += 1
				self.ReportError("Stmt: Unexpected " + self.lex.getTokenName(self.ct) + "; RPAREN_T expected after <action>")
		else:
			errors += self.literal()

		return errors


	def literal(self):
		firsts = []
		follows = []

		errors = 0

		if(self.ct == Token.NUMLIT_T or self.ct == Token.STRLIT_T):
			self.ct = self.lex.getToken()
		elif(self.ct == Token.QUOTE_T):
			self.ct = self.lex.getToken()
			errors += self.quoted_lit()

		return errors


	def quoted_lit(self):
		firsts = []
		follows = []

		errors = 0

		errors += self.any_other_token()

		return errors


	def more_tokens(self):
		firsts = []
		follows = []

		errors = 0

		errors += self.any_other_token()
		errors += self.more_tokens()

		return errors


	def param_list(self):
		firsts = []
		follows = []

		errors = 0

		if(self.ct == Token.IDENT_T):
			self.ct = self.lex.getToken()
			errors += self.param_list()
		else:
			errors += 1
			self.ReportError("Param_List: Unexpected " + self.lex.getTokenName(self.ct) + "; Expected IDENT_T")

		return errors


	def else_part(self):
		firsts = []
		follows = []

		errors = 0

		errors += self.stmt()

		return errors


	def stmt_pair(self):
		firsts = []
		follows = []

		errors = 0

		if(self.ct == Token.LPAREN_T):
			self.ct = self.lex.getToken()
			errors += self.stmt_pair_body()
		else:
			errors += 1
			self.ReportError("Stmt_Pair: Unexpected " + self.lex.getTokenName(self.ct) + "; Expected LPAREN_T")

		return errors


	def stmt_pair_body(self):
		firsts = []
		follows = []

		errors = 0

		if(self.ct == Token.ELSE_T):
			self.ct = self.lex.getToken()
			errors += self.stmt()
			if(self.ct == Token.RPAREN_T):
				self.ct = self.lex.getToken()
			else:
				errors += 1
				self.ReportError("")
		else:
			errors += self.stmt()
			errors += self.stmt()
			if(self.ct == Token.RPAREN_T):
				self.ct = self.lex.getToken()
				errors += self.stmt_pair()
			else:
				errors += 1
				self.ReportError("")

		return errors


	def action(self):
		firsts = []
		follows = []

		errors = 0

		if(self.ct == Token.IF_T):
			self.ct = self.lex.getToken()
			errors += self.stmt()
			errors += self.stmt()
			errors += self.else_part()
		elif(self.ct == Token.COND_T):
			self.ct = self.lex.getToken()
			if(self.ct == Token.LPAREN_T):
				errors += self.stmt_pair_body()
			else:
				errors += 1
				self.ReportError("")
		elif(self.ct == Token.LISTOP_T or self.ct == Token.NOT_T or
		     self.ct == Token.NUMBERP_T or self.ct == Token.SYMBOLP_T or
		     self.ct == Token.LISTP_T or self.ct == Token.ZEROP_T or
		     self.ct == Token.NULLP_T or self.ct == Token.NULLP_T or
		     self.ct == Token.STRINGP_T or self.ct == Token.DISPLAY_T):
			self.ct = self.lex.getToken()
			errors += self.stmt()
		elif(self.ct == Token.AND_T or self.ct == Token.OR_T or
		     self.ct == Token.PLUS_T or self.ct == Token.MULT_T or
		     self.ct == Token.EQUALTO_T or self.ct == Token.GT_T or
		     self.ct == Token.LT_T or self.ct == Token.GTE_T or
		     self.ct == Token.LTE_T or self.ct == Token.IDENT_T):
			self.ct = self.lex.getToken()
			errors += self.stmt_list()
		elif(self.ct == Token.CONS_T or self.ct == Token.MODULO_T):
			self.ct = self.lex.getToken()
			errors += self.stmt()
			errors += self.stmt()
		elif(self.ct == Token.MINUS_T or self.ct == Token.DIV_T):
			self.ct = self.lex.getToken()
			errors += self.stmt()
			errors += self.stmt_list()
		elif(self.ct == Token.NEWLINE_T):
			self.ct = self.lex.getToken()
		else:
			errors += 1
			self.ReportError("Action: You really messed up.")

		return errors


	def any_other_token(self):
		firsts = []
		follows = []

		errors = 0

		if(self.ct == Token.LPAREN_T):
			self.ct = self.lex.getToken()
			errors += self.more_tokens()
			if(self.ct == Token.RPAREN_T):
				self.ct = self.lex.getToken()
			else:
				errors += 1
				self.ReportError("")
		elif(self.ct == Token.QUOTE_T):
			self.ct = self.lex.getToken()
			errors += self.any_other_token()
		elif(self.ct == Token.IDENT_T or self.ct == Token.NUMLIT_T or
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
			self.ct = self.lex.getToken()
		else:
			errors += 1
			self.ReportError("Any_Other_Token: You messed up, bad.")

		return errors


