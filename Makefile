.PHONY: all clean

INNER_MAKE := ./{{ADDON_NAME_PACKAGE}}/Makefile
MAKE_INNER := $(MAKE) -f $(INNER_MAKE)

all: \
	clean \

clean:
	$(MAKE_INNER) clean

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
