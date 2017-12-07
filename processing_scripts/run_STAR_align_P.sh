#!/bin/bash -l

MODULE="$1"
INDEX_DIR="$2"
RUN_THREAD="$3"
SAMPLE_FA_1="$4"
SAMPLE_FA_2="$5"
BAM_FILE="$6"
GZ_ZIPPED="$7"
OTHER="$8"

module load "$MODULE"

cmd="STAR --genomeDir $INDEX_DIR --runThreadN $RUN_THREAD --readFilesIn $SAMPLE_FA_1 $SAMPLE_FA_2 --outFileNamePrefix $BAM_FILE --outSAMtype BAM SortedByCoordinate --outWigType wiggle --quantMode TranscriptomeSAM GeneCounts --outReadsUnmapped Fastx $GZ_ZIPPED $OTHER"

echo $cmd
eval $cmd