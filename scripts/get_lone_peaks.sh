#!/bin/bash

# Check if the correct number of arguments are provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <input_directory> <results_directory>"
    exit 1
fi

INPUT_DIR="$1"
RESULTS_DIR="$2"
OUTPUT_FILE="$RESULTS_DIR/lone_wolf_peaks.bed"

# Create the results directory if it doesn't exist
mkdir -p "$RESULTS_DIR"

# Clear the output file if it already exists
> "$OUTPUT_FILE"

# Find all .narrowPeak files in the input directory and store them in an array
shopt -s nullglob
files=("$INPUT_DIR"/*.bed)
shopt -u nullglob

if [ ${#files[@]} -eq 0 ]; then
    echo "No .bed files found in $INPUT_DIR. Exiting."
    exit 1
fi

# Loop through each .narrowPeak file for the primary comparison
for query_file in "${files[@]}"; do
    echo "Processing $(basename "$query_file")..."

    # Create a temporary file to hold all other peaks
    temp_others="$RESULTS_DIR/temp_others.bed"
    > "$temp_others"

    # Concatenate all files *except* the current query file
    for other_file in "${files[@]}"; do
        if [ "$query_file" != "$other_file" ]; then
            cat "$other_file" >> "$temp_others"
        fi
    done

    # Use bedtools intersect with the -v option to find peaks in the current file
    # that do not overlap with any other peaks.
    # The output is appended to the main results file.
    bedtools intersect -a "$query_file" -b "$temp_others" -v >> "$OUTPUT_FILE"

    # Clean up the temporary file
    rm "$temp_others"
done

echo "Lone wolf peaks have been saved to $OUTPUT_FILE"