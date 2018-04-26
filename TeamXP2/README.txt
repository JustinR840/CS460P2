CS 460 Project 2
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
	The program can also perform basic error recovery.


WHAT DOESN'T WORK:
	There seems to be a problem in the output of what rule is being
	used. In a few instances the rule used differs from the expected
	(seemingly?), but the code still comes out as error free. I
	haven't been able to determine what is causing this issue.
