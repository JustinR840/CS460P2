run :
	cp $(FILE) Python
	cd Python; /usr/local/bin/python3.6 main.py $(FILE)

clean :
	rm -rf Python/__pycache__
	cd Python; rm -f *.p1 *.p2 *.lst *.dbg *.ss

submit : clean
	cd Python; rm -f input.ss
	cd ..; tar cfvz TeamXP2.tgz TeamXP2
	cd ..; cp TeamXP2.tgz ~tiawatts/cs460drop
