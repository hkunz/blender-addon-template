.PHONY: all clean documentation

INNER_MAKE := ./{{ADDON_NAME_PACKAGE}}/Makefile
MAKE_INNER := $(MAKE) -f $(INNER_MAKE)

all:
	$(MAKE_INNER) all

clean:
	$(MAKE_INNER) clean

documentation:
	$(MAKE_INNER) documentation

documentation-content-final:
	$(MAKE_INNER) documentation-content-final

documentation-pdf:
	$(MAKE_INNER) documentation-pdf

create-next-tag:
	$(MAKE_INNER) create-next-tag

zip:
	$(MAKE_INNER) zip

fix-py-permissions:
	$(MAKE_INNER) fix-py-permissions

configure:
	@echo "=====================================================================================>"
	@echo "Configure Start ..."
	./scripts/configure.sh
