#!/bin/bash -l

MODULE="$1"
BAM="$2"

module load "$MODULE"

samtools index "$BAM"