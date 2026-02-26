#!/bin/bash
# Generate PDF from markdown whitepaper using pandoc
# Usage: generate-pdf.sh <input.md> <output.pdf> [--toc] [--template=<path>]

set -euo pipefail

INPUT="${1:?Usage: generate-pdf.sh <input.md> <output.pdf> [--toc] [--template=<path>]}"
OUTPUT="${2:?Usage: generate-pdf.sh <input.md> <output.pdf> [--toc] [--template=<path>]}"

# Parse optional arguments
TOC=""
TEMPLATE=""
for arg in "${@:3}"; do
    case "$arg" in
        --toc) TOC="--toc --toc-depth=3" ;;
        --template=*) TEMPLATE="--template=${arg#--template=}" ;;
    esac
done

# Check for pandoc
if ! command -v pandoc &>/dev/null; then
    echo "ERROR: pandoc is not installed."
    echo ""
    echo "Install pandoc:"
    echo "  macOS:   brew install pandoc"
    echo "  Ubuntu:  sudo apt-get install pandoc"
    echo "  Windows: choco install pandoc"
    echo ""
    echo "For PDF generation, you also need a LaTeX engine:"
    echo "  macOS:   brew install --cask mactex-no-gui"
    echo "  Ubuntu:  sudo apt-get install texlive-xetex"
    echo "  Windows: choco install miktex"
    echo ""
    echo "Alternative (no LaTeX needed):"
    echo "  pip install weasyprint"
    echo "  pandoc \"$INPUT\" -o \"$OUTPUT\" --pdf-engine=weasyprint"
    exit 1
fi

# Detect available PDF engine
PDF_ENGINE=""
if command -v xelatex &>/dev/null; then
    PDF_ENGINE="--pdf-engine=xelatex"
elif command -v pdflatex &>/dev/null; then
    PDF_ENGINE="--pdf-engine=pdflatex"
elif command -v lualatex &>/dev/null; then
    PDF_ENGINE="--pdf-engine=lualatex"
elif command -v weasyprint &>/dev/null; then
    PDF_ENGINE="--pdf-engine=weasyprint"
elif command -v wkhtmltopdf &>/dev/null; then
    PDF_ENGINE="--pdf-engine=wkhtmltopdf"
else
    echo "ERROR: No PDF engine found."
    echo "Install one of: xelatex, pdflatex, lualatex, weasyprint, wkhtmltopdf"
    echo ""
    echo "Quickest option:"
    echo "  pip install weasyprint"
    exit 1
fi

echo "Generating PDF..."
echo "  Input:      $INPUT"
echo "  Output:     $OUTPUT"
echo "  PDF Engine: ${PDF_ENGINE#--pdf-engine=}"
echo "  TOC:        ${TOC:-disabled}"

# Build pandoc command
# shellcheck disable=SC2086
pandoc "$INPUT" \
    -o "$OUTPUT" \
    $PDF_ENGINE \
    $TOC \
    ${TEMPLATE:+$TEMPLATE} \
    --variable=geometry:margin=1in \
    --variable=fontsize:11pt \
    --variable=colorlinks:true \
    --variable=linkcolor:NavyBlue \
    --variable=urlcolor:NavyBlue \
    --highlight-style=tango \
    --number-sections \
    --standalone

echo "PDF generated: $OUTPUT"
echo "Size: $(du -h "$OUTPUT" | cut -f1)"
