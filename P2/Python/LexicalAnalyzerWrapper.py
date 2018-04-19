from ctypes import *
from platform import system

class LexicalAnalyzerWrapper(object):
	libDir = "../Lib/"
	# TODO: Standardize these names
	winLib = libDir + "CS460P2.dll"
	linuxLib = libDir + "LibLex.so"

	# TODO: These should go to a debug log, NOT standard output
	# TODO: Should this be in main?
	if(system() == "Windows"):
		#print("OS is Windows - Using CS460P2.dll")
		lib = cdll.LoadLibrary(winLib)
	elif(system() == "Linux"):
		#print("OS is Linux - Using LibLex.so")
		lib = cdll.LoadLibrary(linuxLib)
	else:
		raise Exception("Unsupported operating system")


	Lex_New = lib.LexicalAnalyzer_New
	Lex_Destructor = lib.LexicalAnalyzer_Destructor

	# We're going to wrap these
	_Lex_GetLexeme = lib.LexicalAnalyzer_GetLexeme
	_Lex_GetToken = lib.LexicalAnalyzer_GetToken
	_Lex_GetTokenName = lib.LexicalAnalyzer_GetTokenName
	_Lex_FreeChar = lib.LexicalAnalyzer_FreeChar


	def __init__(self):
		# Set required parameters for each functions
		self.Lex_New.argtypes = [c_char_p]
		self._Lex_FreeChar.argtypes = [c_void_p]
		# self._Lex_GetLexeme.argtypes = []

		# Set return type for each function
		self.Lex_New.restype = c_void_p
		self._Lex_FreeChar.restype = None
		self._Lex_GetLexeme.restype = c_void_p
		self._Lex_GetTokenName.restype = c_void_p

	def Lex_GetLexeme(self, lex):
		ptr = self._Lex_GetLexeme(lex)
		lexeme = cast(ptr, c_char_p).value.decode("utf-8")
		self._Lex_FreeChar(ptr)
		return lexeme

	def Lex_GetToken(self, lex):
		token = self._Lex_GetToken(lex)
		return token

	def Lex_GetTokenName(self, lex, t):
		ptr = self._Lex_GetTokenName(lex, t)
		lexeme = cast(ptr, c_char_p).value.decode("utf-8")
		self._Lex_FreeChar(ptr)
		return lexeme