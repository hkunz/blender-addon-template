.PHONY: all clean documentation

version ?= -i

all: \
	clean \
	documentation

documentation: \
	documentation-content-final \
	documentation-pdf

documentation-content-final:
	@echo "=====================================================================================>"
	@echo "Generating documentation content file ..."
	./scripts/generate-documentation-content-html.sh

documentation-pdf:
	@echo "=====================================================================================>"
	@echo "Generating documentation PDF ..."
	./scripts/convert-html-to-pdf.sh resources/documentation/content/latest/final/documentation-content.html

create-next-tag:
	@echo "=====================================================================================>"
	@echo "Create new tag ..."
	./scripts/create-tag.sh $(version)

zip:
	./scripts/build-zip.sh

fix-py-permissions:
	find . -type f -name '*.py' -exec chmod 755 {} +

clean:
	@echo "=====================================================================================>"
	@echo "Cleaning ..."
	find . -type d -name '__pycache__' -exec rm -r {} +

configure:
	@echo "=====================================================================================>"
	@echo "Configure Start ..."
	./scripts/configure.sh
