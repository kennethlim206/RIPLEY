#!/bin/bash -l

MODULE="$1"
CUSTOM_ANNO="$2"
FEATURE_DIR="$3"
ALIGN_DIR="$4"
PAIRED="$5"
OTHER="$6"

module load "$MODULE"

cmd="featureCounts $PAIRED $OTHER -g gene_id -a $CUSTOM_ANNO -o $FEATURE_DIR $ALIGN_DIR"

echo $cmd
eval $cmd
