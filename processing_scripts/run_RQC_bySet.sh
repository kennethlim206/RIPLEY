#!/bin/bash -l

module load rseqc/2.6.3

OUTPUT_DIR="$1"
INPUT_FILE="$2"
REFERENCE_GENOME="$3"

geneBody_coverage.py -f pdf -i "$INPUT_FILE" -o "$OUTPUT_DIR" -r "$REFERENCE_GENOME"