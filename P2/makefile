libfoo.so : foo.o
	g++ -shared -Wl,-soname,libfoo.so -o libfoo.so foo.o

foo.o : foo.cpp
	g++ -c -fPIC foo.cpp -o foo.o

run : libfoo.so fooWrapper.py main.py
	python3 main.py

clean :
	rm -f *.o *.so
	rm -rf __pycache__
