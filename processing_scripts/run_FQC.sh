#!/bin/bash -l

module load fastqc/v0.11.2

OUTPUT_DIR="$1"
FASTQ_FILE="$2"

cmd="fastqc -o $OUTPUT_DIR $FASTQ_FILE"

echo $cmd
eval $cmd
