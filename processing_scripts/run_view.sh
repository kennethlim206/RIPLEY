#!/bin/bash -l

MODULE="$1"
PROCESSING_DIR="$2"
INPUT_DIR="$3"
AMP_DIR="$4"
OUT_DIR="$5"

module load "$MODULE"

python "$PROCESSING_DIR"/run_view.py "$PROCESSING_DIR" "$INPUT_DIR" "$AMP_DIR" "$OUT_DIR"