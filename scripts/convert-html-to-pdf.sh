#!/bin/bash

DOC_DIR="resources/documentation/"
PDF_OUT="${DOC_DIR}documentation.pdf"
DEFAULT_DOC="${DOC_DIR}content/latest/final/documentation-content.html"

if [ -z "$1" ]; then
    echo "Error: Please specify a file path."
    echo "Example: $0 ${DEFAULT_DOC}"
    exit 1
fi

if [ ! -f "$1" ]; then
    echo "Error: '$1' does not exist."
    exit 1
fi

CONTENT=$(< "$1")
HEADERS="$(tr -d '\n' <"${DOC_DIR}documentation-simple.html" | sed -E "s/(<body[^>]*>).*$/\1\n/")"
HTML="${HEADERS}${CONTENT}</body></html>"

TEMP_FILE=$(mktemp /tmp/tempfile.XXXXXX.html)
cleanup() {
    rm -f "$TEMP_FILE"
    exit 1
}
HTML=$(echo "$HTML" | sed -e 's/<h4/<h1/g' -e 's/<h6/<h3/g')
echo "$HTML" > "$TEMP_FILE"
trap cleanup SIGINT
wkhtmltopdf --page-size A4 --margin-top 10mm --margin-bottom 10mm --margin-left 10mm --margin-right 10mm "$TEMP_FILE" "${PDF_OUT}"
rm -f "$TEMP_FILE"