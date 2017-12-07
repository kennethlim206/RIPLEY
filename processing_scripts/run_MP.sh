#!/bin/bash -l

MODULE="$1"
USE_FA="$2"
BAM="$3"
OUTPUT="$4"
CHROM="$5"
START="$6"
END="$7"
OTHER="$8"

module load "$MODULE"

cmd="samtools mpileup -u -v $OTHER -f $USE_FA --region $CHROM:$START-$END --output $OUTPUT $BAM"

echo $cmd
eval $cmd