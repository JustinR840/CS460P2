LibLex.so : Project2.so_o SetLimits.so_o LexicalAnalyzer.so_o SyntacticalAnalyzer.so_o LexicalAnalyzerInterface.so_o
	g++ -shared -Wl,-soname,LibLex.so Project2.so_o SetLimits.so_o LexicalAnalyzer.so_o SyntacticalAnalyzer.so_o LexicalAnalyzerInterface.so_o -o LibLex.so

Project2.so_o : Project2.cpp SetLimits.h SyntacticalAnalyzer.h
	g++ -c -fPIC -std=c++11 Project2.cpp -o Project2.so_o

SetLimits.so_o : SetLimits.cpp SetLimits.h
	g++ -c -fPIC -std=c++11 SetLimits.cpp -o SetLimits.so_o

LexicalAnalyzer.so_o : LexicalAnalyzer.cpp LexicalAnalyzer.h
	g++ -c -fPIC -std=c++11 LexicalAnalyzer.cpp -o LexicalAnalyzer.so_o

LexicalAnalyzerInterface.so_o : LexicalAnalyzerInterface.cpp LexicalAnalyzerInterface.h
	g++ -c -fPIC -std=c++11 LexicalAnalyzerInterface.cpp -o LexicalAnalyzerInterface.so_o

SyntacticalAnalyzer.so_o : SyntacticalAnalyzer.cpp SyntacticalAnalyzer.h LexicalAnalyzer.h
	g++ -c -fPIC -std=c++11 SyntacticalAnalyzer.cpp -o SyntacticalAnalyzer.so_o

clean : 
	rm -f *.so_o *.so *.gch
