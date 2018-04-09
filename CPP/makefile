P1.out : Project1.o SetLimits.o LexicalAnalyzer.o SyntacticalAnalyzer.o
	g++ -std=c++11 -g -o P1.out Project1.o SetLimits.o LexicalAnalyzer.o SyntacticalAnalyzer.o

Project1.o : Project1.cpp SetLimits.h SyntacticalAnalyzer.h
	g++ -std=c++11 -g -c Project1.cpp

SetLimits.o : SetLimits.cpp SetLimits.h
	g++ -std=c++11 -g -c SetLimits.cpp

LexicalAnalyzer.o : LexicalAnalyzer.cpp LexicalAnalyzer.h
	g++ -std=c++11 -g -c LexicalAnalyzer.cpp

SyntacticalAnalyzer.o : SyntacticalAnalyzer.cpp SyntacticalAnalyzer.h LexicalAnalyzer.h
	g++ -std=c++11 -g -c SyntacticalAnalyzer.cpp

clean : 
	rm -f *.o *.out *.gch *.so *.so_o

submit : Project1.cpp LexicalAnalyzer.h LexicalAnalyzer.cpp SyntacticalAnalyzer.h SyntacticalAnalyzer.cpp makefile README.txt
	rm -rf yourlastnameP1
	mkdir yourlastnameP1
	cp Project1.cpp yourlastnameP1
	cp LexicalAnalyzer.h yourlastnameP1
	cp LexicalAnalyzer.cpp yourlastnameP1
	cp SyntacticalAnalyzer.h yourlastnameP1
	cp SyntacticalAnalyzer.cpp yourlastnameP1
	cp makefile yourlastnameP1
	cp README.txt yourlastnameP1
	tar cfvz yourlastnameP1.tgz yourlastnameP1
	cp yourlastnameP1.tgz ~tiawatts/cs460drop

SO : Project1.so_o SetLimits.so_o LexicalAnalyzer.so_o SyntacticalAnalyzer.so_o
	g++ -shared -Wl,-soname,LibP1.so -o LibP1.so Project1.so_o SetLimits.so_o LexicalAnalyzer.so_o SyntacticalAnalyzer.so_o

Project1.so_o : Project1.cpp SetLimits.h SyntacticalAnalyzer.h
	g++ -std=c++11 -fPIC -g -c Project1.cpp -o Project1.so_o

SetLimits.so_o : SetLimits.cpp SetLimits.h
	g++ -std=c++11 -fPIC -g -c SetLimits.cpp -o SetLimits.so_o

LexicalAnalyzer.so_o : LexicalAnalyzer.cpp LexicalAnalyzer.h
	g++ -std=c++11 -fPIC -g -c LexicalAnalyzer.cpp -o LexicalAnalyzer.so_o

SyntacticalAnalyzer.so_o : SyntacticalAnalyzer.cpp SyntacticalAnalyzer.h LexicalAnalyzer.h
	g++ -std=c++11 -fPIC -g -c SyntacticalAnalyzer.cpp -o SyntacticalAnalyzer.so_o
