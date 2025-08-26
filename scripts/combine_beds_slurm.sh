#!/bin/bash 

#SBATCH --job-name=uniwig_combine_narrowpeaks
#SBATCH --ntasks=1
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1  
#SBATCH --mem='32000'
#SBATCH --cpus-per-task='8'
#SBATCH --partition=standard
#SBATCH --time=2:00:00
#SBATCH -o t1d_output.out
#SBATCH -e t1d_output.err

# Directory for the raw data (narrowPeak files)
RAWDATA_DIR="/home/drc/Downloads/test_sorting/input/"

# Directory for combined data
COMBDATA_DIR="/home/drc/Downloads/test_sorting/output/"

# Make sure the output directory exists
mkdir -p "$COMBDATA_DIR"

# unsorted combined data filename
unsorted="combined_unsort.narrowPeak"

# chrsorted combined data filename
chrsorted="combined_chrsort.narrowPeak"

# Use find to locate all .narrowPeak files and pass them to cat
# The -exec option is more robust than a pipe and a while loop for this simple task
# It finds all matching files and concatenates them into the output file
find "$RAWDATA_DIR" -type f -name "*.narrowPeak" -exec cat {} + > "$COMBDATA_DIR$unsorted"

# Check if the unsorted file was created successfully before attempting to sort
if [ -s "$COMBDATA_DIR$unsorted" ]; then
  # Sort the merged file by chromosome and location
  sort -k1,1 -k2,2n "$COMBDATA_DIR$unsorted" > "$COMBDATA_DIR$chrsorted"
  echo "Sorting and merging complete."

  # Optional: Remove the intermediate unsorted file to save space
  # rm "$COMBDATA_DIR$unsorted"
else
  echo "Error: No .narrowPeak files found in '$RAWDATA_DIR'. The combined file was not created."
fi