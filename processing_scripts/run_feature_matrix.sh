#!/bin/bash

WORKING_DIR="$1"
INPUT_DIR="$2"

python "$WORKING_DIR"/feature_matrix.py "$INPUT_DIR"