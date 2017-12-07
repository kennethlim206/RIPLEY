#!/bin/bash -l

OUTPUT_DIR="$1"
FTP_COMMAND="$2"

# wget -r -np -nd -nH -N -P "$OUTPUT_DIR" -R index.html* "$FTP_COMMAND"

cmd="rsync -avL slimsdata.genomecenter.ucdavis.edu::slims/$FTP_COMMAND $OUTPUT_DIR"

echo "$cmd"
eval "$cmd"