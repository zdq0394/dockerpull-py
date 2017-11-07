clean_pyc:
	rm -fr hubsync/*.pyc
	rm -fr hubsync/http_client/*.pyc

clean_out:
	rm -fr data/result

clean: clean_pyc clean_out

run:
	python hubsync/main.py -c conf/config.ini
