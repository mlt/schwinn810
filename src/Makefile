#!/usr/bin/make -f

SUBDIRS = core

all: $(SUBDIRS)
#doc

$(SUBDIRS):
	$(MAKE) -C $@

apidoc:
	sphinx-apidoc --force -o doc/source .

#export PYTHONPATH:= "${OSGEO4W_ROOT}/apps/qgis/python;${OSGEO4W_ROOT}/apps/qgis/python/plugins;${HOME}/.qgis/python/plugins;${OSGEO4W_ROOT}/apps/python27/lib/site-packages"
#export PATH:= "${PATH}:${OSGEO4W_ROOT}/bin:${OSGEO4W_ROOT}/bin:${OSGEO4W_ROOT}/apps/qgis/bin:${OSGEO4W_ROOT}/apps/qgis/plugins:${OSGEO4W_ROOT}/apps/Python27/Scripts"

doc: apidoc
	$(MAKE) -C doc html
# cd doc && cmd \\/c make.bat html

# @PATH=${PATH} echo %PATH%
# @PATH=${PATH} $(MAKE) -C doc html

zip:
	7z a -r -x!.ropeproject -x!doc schwinn810.zip ".\*.py"

.PHONY: subdirs $(SUBDIRS) apidoc doc
