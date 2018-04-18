import LexicalAnalyzerWrapper

class LexicalAnalyzer(object):
	def __init__(self, filename):
		# Initialize the wrapper
		self.Wrapper = LexicalAnalyzerWrapper.LexicalAnalyzerWrapper()
		# Create the lexical analyzer
		self.lex = self.Wrapper.Lex_New(filename)

	# Called when this object is freed from memory.
	# We need to make sure we call the destructor
	# for the lexical analyzer.
	def __del__(self):
		self.Wrapper.Lex_Destructor(self.lex)

	def getLexeme(self):
		return self.Wrapper.Lex_GetLexeme(self.lex)

	def getToken(self):
		return self.Wrapper.Lex_GetToken(self.lex)

	def getTokenName(self, token):
		return self.Wrapper.Lex_GetTokenName(self.lex, token)

	def ReportError(self, err):
		print(err)
		# We're not going to use the error handling for the
		# lexical analyzer I think. We'll implement our own