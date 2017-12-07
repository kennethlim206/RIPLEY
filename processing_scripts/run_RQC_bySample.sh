#!/bin/bash -l

module load rseqc/2.6.3

OUTPUT_DIR="$1"
INPUT_FILE="$2"
REFERENCE_GENOME="$3"

RPKM_saturation.py -i "$INPUT_FILE" -o "$OUTPUT_DIR" -r "$REFERENCE_GENOME"

FPKM_count -i "$INPUT_FILE" -o "$OUTPUT_DIR" -r "$REFERENCE_GENOME"

bam_stat.py -i "$INPUT_FILE"

read_GC.py -i "$INPUT_FILE"