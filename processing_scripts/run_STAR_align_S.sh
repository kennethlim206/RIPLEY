#!/bin/bash -l

MODULE="$1"
INDEX_DIR="$2"
RUN_THREAD="$3"
SAMPLE_FA="$4"
BAM_FILE="$5"
GZ_ZIPPED="$6"
OTHER="$7"

module load "$MODULE"

cmd="STAR --genomeDir $INDEX_DIR --runThreadN $RUN_THREAD --readFilesIn $SAMPLE_FA --outFileNamePrefix $BAM_FILE --outSAMtype BAM SortedByCoordinate --outWigType wiggle --quantMode TranscriptomeSAM GeneCounts --outReadsUnmapped Fastx $GZ_ZIPPED $OTHER"

echo $cmd
eval $cmd