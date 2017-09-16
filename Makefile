clean_pyc:
	rm -fr lib/*.pyc

clean_out:
	rm -fr out/*

clean: clean_pyc clean_out