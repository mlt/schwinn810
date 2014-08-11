# handy stuff

ui_%.py : %.ui
	python -m PyQt4.uic.pyuic -x -o $@ $^

