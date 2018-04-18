import LexicalAnalyzerWrapper

class LexicalAnalyzer(object):
	def __init__(self, filename):
		# Initialize the wrapper
		# While this works, I don't like it. We're loading the library again every
		# time we create a Lexical Analyzer class. I think perhaps if we declare
		# this outside of init, it'll just be static to every LexicalAnalyzer object.
		# TODO: Need to do some testing on this later.
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