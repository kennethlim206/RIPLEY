#!/bin/bash

WORKING_DIR="$1"
REF="$2"
ADD="$3"
CUSTOM="$4"

python "$WORKING_DIR"/cat.py "$REF" "$ADD" "$CUSTOM"