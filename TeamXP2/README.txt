CS 460 Project 2 - Checkpoint
Authors: Adam May
	 Justin Ramos

HOW TO RUN:
	While in the base directory (the one containing the makefile)
	just execute the follow command:
	make run FILE=<filename>
	where <filename> is the input file to be processed. This file
	should be in the same directory as the makefile. What will happen
	once that command is run is:
		1. The input file will be copied into the Python directory
		2. The make shell will enter the python directory and
			execute main.py with the input file as an argument.
			Specifically it will run:
			python3.6 main.py $(FILE)


OUTPUT:
	The output files will be in the Python directory.


WHAT WORKS:
	The program is able to sucessfully parse error free scheme code
	that follow the syntactical rules of the project.


WHAT DOESN'T WORK:
	Everything works according to the checkpoint specifications. The
	following items are areas that need to be improved upon for part 2
	of the project.
		1. The C++ LexicalAnalyzer class needs some tweaks. I really
			wanted to avoid touching ANYTHING related to it more
			for the experience of "dealing with the cards I'd been
			dealt."
		2. Firsts and follows are not implemented in an efficient way.
			This absolutely needs to be redone. They'll likely end
			up getting stored in a table for part 2.
		3. The LexicalAnalyzerWrapper class could use some cleanup,
			especially with how a LexicalAnalyzer created a new
			wrapper class every single time a new analyzer is made.
