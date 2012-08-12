DESTDIR=/usr

.PHONY: all ui install

all: ui

ui:
	$(MAKE) -C src

CORE=commands.py \
device.py \
__init__.py \
progress_gtk.py \
progress.glade \
progress_qt.py \
ui_progress.py \
progress_text.py \
reader_cresta.py \
reader.py \
reader_schwinn.py \
utils.py \
writer_csv.py

EXTRA=__init__.py \
writer_sqlite.py

SRC=csv2tcx.py \
download.py \
settings.py

install:
	mkdir -p $(DESTDIR)/share/schwinn810
	install -m 0755 $(addprefix src/, $(SRC)) $(DESTDIR)/share/schwinn810/

	mkdir -p $(DESTDIR)/share/schwinn810/core
	install -m 0644 $(addprefix src/core/, $(CORE)) $(DESTDIR)/share/schwinn810/core/

	mkdir -p $(DESTDIR)/share/schwinn810/extra
	install -m 0644 $(addprefix src/extra/, $(EXTRA)) $(DESTDIR)/share/schwinn810/extra/

	mkdir -p $(DESTDIR)/share/schwinn810/web
	install -m 0644 src/web/mmf.py src/web/tcx2web.py $(DESTDIR)/share/schwinn810/web/

	mkdir -p $(DESTDIR)/share/schwinn810/web/antd
	install -m 0644 src/web/antd/*.py src/web/antd/LICENSE $(DESTDIR)/share/schwinn810/web/antd/

	mkdir -p $(DESTDIR)/bin
	install -m 0755 linux/schwinn810 $(DESTDIR)/bin/
	install -m 0755 linux/babelize.sh linux/schwinn810-tray.py $(DESTDIR)/share/schwinn810/
