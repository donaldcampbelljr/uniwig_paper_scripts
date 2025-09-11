# This script generates a random narrowPeak file for a single chromosome.

import argparse
import random
import sys
import os

def generate_narrowpeak_file(
    num_lines: int,
    output_filename: str,
    output_dir: str,
    high_score_percentage: float,
    spike: float
):
    """
    Generates a narrowPeak file with random, yet valid, peak data.

    Args:
        num_lines (int): The number of lines (peaks) to generate.
        output_filename (str): The name of the output file.
        output_dir (str): The directory where the file will be saved.
        high_score_percentage (float): The percentage of scores to be
                                       "super high" (900-1000). Must be
                                       between 0.0 and 1.0.
    """
    # The length of chromosome 1 in the hg38 reference genome.
    # This value is used to ensure all start/end coordinates are valid.
    CHR1_LENGTH = 248956422
    
    # Check if the high score percentage is within a valid range.
    if not 0.0 <= high_score_percentage <= 1.0:
        print("Error: The high score percentage must be between 0.0 and 1.0.", file=sys.stderr)
        return

    # Create the output directory if it does not exist.
    try:
        os.makedirs(output_dir, exist_ok=True)
    except OSError as e:
        print(f"Error: Could not create directory '{output_dir}'. {e}", file=sys.stderr)
        return

    # Construct the full path for the output file.
    output_path = os.path.join(output_dir, output_filename)

    try:
        with open(output_path, 'w') as f:

            for i in range(num_lines):
                # Generate a random peak width between 10 and 1000 bp.
                peak_width = random.randint(10, 1000)

                # Generate a random start position for the peak.
                # The start position is chosen such that the end position does
                # not exceed the chromosome length.
                chrom_start = random.randint(0, CHR1_LENGTH - peak_width)
                chrom_end = chrom_start + peak_width

                # Column 4 can be a placeholder name.
                name = "SYNTHETIC"

                # Generate the score with a skewed distribution.
                # If a random number is less than the specified percentage,
                # the score is in the "super high" range (900-1000).
                # Otherwise, it's in the standard range (0-900).
                if random.random() < high_score_percentage:
                    score = random.randint(900, 1000)
                else:
                    score = random.randint(0, 900)

                # The rest of the narrowPeak columns are not required by the user,
                # so they are set to placeholder values.
                strand = "."
                signal_value = 0
                p_value = 0
                q_value = 0
                peak = 0

                # Format the line according to the narrowPeak specification.
                line = (
                    f"chr1\t{chrom_start}\t{chrom_end}\t{name}\t{score}\t{strand}\t"
                    f"{signal_value}\t{p_value}\t{q_value}\t{peak}\n"
                )
                f.write(line)
            
            if spike > 0:
                for i in range(spike):
                    peak_width = random.randint(10, 1000)
                    chrom_start = random.randint(0, CHR1_LENGTH - peak_width)
                    chrom_end = chrom_start + peak_width

                    name = "SPIKE_SYNTHETIC"

                    score = random.randint(1200, 1400)

                    strand = "."
                    signal_value = 0
                    p_value = 0
                    q_value = 0
                    peak = 0

                    # Format the line according to the narrowPeak specification.
                    line = (
                        f"chr1\t{chrom_start}\t{chrom_end}\t{name}\t{score}\t{strand}\t"
                        f"{signal_value}\t{p_value}\t{q_value}\t{peak}\n"
                    )
                    f.write(line)


        print(f"Successfully generated {num_lines} random peaks and saved to '{output_path}'")
    except IOError as e:
        print(f"Error: Could not write to file '{output_path}'. {e}", file=sys.stderr)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate a random narrowPeak file.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        "-n", "--num_lines",
        type=int,
        default=1000,
        help="The number of lines (peaks) to generate (maximum 1000)."
    )

    parser.add_argument(
        "-o", "--output_file",
        type=str,
        default="random_peaks.narrowPeak",
        help="The name of the output file."
    )

    parser.add_argument(
        "-d", "--output_dir",
        type=str,
        default="output",
        help="The directory to save the output file."
    )

    parser.add_argument(
        "-s", "--high_score_percentage",
        type=float,
        default=0.1,
        help="The percentage of scores that should be 'super high' (900-1000). "
             "Must be a value between 0.0 and 1.0."
    )

    parser.add_argument(
        "-p", "--spike",
        type=int,
        default=0,
        help="The number of lines to spike into file at 1.30 max value"
    )
    
    args = parser.parse_args()

    # Clamp the number of lines to a maximum of 1000.
    if args.num_lines > 1000:
        print("Warning: Limiting the number of lines to the maximum of 1000.", file=sys.stderr)
        args.num_lines = 1000

    generate_narrowpeak_file(
        num_lines=args.num_lines,
        output_filename=args.output_file,
        output_dir=args.output_dir,
        high_score_percentage=args.high_score_percentage,
        spike=args.spike
    )