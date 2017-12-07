#!/bin/bash -l

module load bedtools2/2.21.0

F="$1"
BAM="$2"
BED="$3"
OUTPUT="$4"

cmd="bedtools multicov -f $F -bams $BAM -bed $BED > $OUTPUT"

echo "$cmd"
eval "$cmd"