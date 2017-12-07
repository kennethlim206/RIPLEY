#!/bin/bash -l

BAM="$1"
POS="$2"

samtools view -c "$BAM" "$POS"