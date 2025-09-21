#!/bin/bash

# Check for correct number of arguments
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <input_bed_file> <output_bed_file>"
    exit 1
fi

INPUT_FILE="$1"
OUTPUT_FILE="$2"
TEMP_SCORES_FILE="temp_scores.txt"

# --- Step 1: Calculate the 75th percentile ---

# Extract the 5th column (scores) from the input file
awk '{print $5}' "$INPUT_FILE" > "$TEMP_SCORES_FILE"

# Sort the scores and use awk to find the 75th percentile value
PERCENTILE_75=$(sort -n "$TEMP_SCORES_FILE" | awk 'BEGIN{n=0;}{s[n]=$0;n++;}END{pos=int(n*0.75); if (pos > 0 && pos < n) print s[pos]; else if (n > 0) print s[n-1]; else print 0;}')

# --- Step 2: Filter the file based on the threshold ---

# Use awk to filter the input file, printing only lines with a score > the threshold
awk -v threshold="$PERCENTILE_75" '$5 > threshold {print}' "$INPUT_FILE" > "$OUTPUT_FILE"

# Clean up the temporary scores file
rm "$TEMP_SCORES_FILE"

echo "Filtering complete. High-scoring peaks are saved to $OUTPUT_FILE"