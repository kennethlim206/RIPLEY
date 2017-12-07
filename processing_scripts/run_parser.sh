#!/bin/bash -l

WORKING_DIR="$1"
INPUT_DIR="$2"
OUTPUT_DIR="$3"

python "$WORKING_DIR"/mp_parser.py "$INPUT_DIR" "$OUTPUT_DIR"