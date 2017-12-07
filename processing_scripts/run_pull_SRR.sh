#!/bin/bash -l

module load sratoolkit

OUTPUT_DIR="$1"
FASTQ_NAME="$2"

fastq-dump --outdir "$OUTPUT_DIR" --gzip -I --split-files "$FASTQ_NAME"