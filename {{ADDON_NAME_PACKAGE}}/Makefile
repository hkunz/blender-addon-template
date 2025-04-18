.PHONY: all clean

MAKEFILE_DIR := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

version ?= -i

all: \
	clean \

documentation: \
	documentation-content-final \
	documentation-pdf

documentation-content-final:
	@echo "=====================================================================================>"
	@echo "Generating documentation content file ..."
	$(MAKEFILE_DIR)/scripts/generate-documentation-content-html.sh

documentation-pdf:
	@echo "=====================================================================================>"
	@echo "Generating documentation PDF ..."
	$(MAKEFILE_DIR)/scripts/convert-html-to-pdf.sh resources/documentation/content/latest/final/documentation-content.html

create-next-tag:
	@echo "=====================================================================================>"
	@echo "Create new tag ..."
	$(MAKEFILE_DIR)/scripts/create-tag.sh $(version)

zip:
	./scripts/build-zip.sh

fix-py-permissions:
	find . -type f -name '*.py' -exec chmod 755 {} +

clean:
	@echo "=====================================================================================>"
	@echo "Cleaning ..."
	find . -type d -name '__pycache__' -exec rm -r {} +
