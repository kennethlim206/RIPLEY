#!/bin/bash

MODULE="$1"
RUN_THREAD="$2"
SJBD_OVERHANG="$3"
INDEX_DIR="$4"
CUSTOM_FA="$5"
CUSTOM_ANNO="$6"
OTHER="$7"

module load "$MODULE"

cmd="STAR --runMode genomeGenerate --runThreadN $RUN_THREAD --genomeDir $INDEX_DIR --genomeFastaFiles $CUSTOM_FA --sjdbGTFfile $CUSTOM_ANNO --sjdbOverhang $SJBD_OVERHANG $OTHER"

echo $cmd
eval $cmd