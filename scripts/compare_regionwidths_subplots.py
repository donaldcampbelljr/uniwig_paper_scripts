# This script analyzes genomic region width distributions from multiple BED or narrowPeak files

import pandas as pd
import matplotlib.pyplot as plt
import os
import math

# INPUT_DATA_DIR = "/home/drc/Downloads/GTARS_PAPER/sample_list/atac_seq_15/"
# RESULTS_DIR = "/home/drc/Downloads/GTARS_PAPER/PROCESSED/atacseq15_regionwidths/"

INPUT_DATA_DIR = "/home/drc/Downloads/GTARS_PAPER/sample_list/atac_seq_15/"
RESULTS_DIR = "/home/drc/Downloads/narrowpeakgeneration/experiment4/stats_figs/region_widths/"


# Define the number of subplots per figure to maintain readability.
SUBPLOTS_PER_FIGURE = 6

def analyze_bed_files_in_directory(input_dir):
    """
    Analyzes all .bed and .narrowPeak files in the given directory.

    Args:
        input_dir (str): The path to the directory containing the files.
    """
    try:
        # Check if the results directory exists, and create it if it doesn't.
        if not os.path.exists(RESULTS_DIR):
            os.makedirs(RESULTS_DIR)
            print(f"Created results directory: {RESULTS_DIR}")

        # List all files in the input directory that are either .bed or .narrowPeak.
        all_files = [
            os.path.join(input_dir, f)
            for f in os.listdir(input_dir)
            if f.endswith(('.bed', '.narrowPeak'))
        ]

        if not all_files:
            print(f"No .bed or .narrowPeak files found in '{input_dir}'. Exiting.")
            return

        print(f"Found {len(all_files)} files to analyze. Processing...")

        # Process files in chunks to create multi-subplot figures.
        for i in range(0, len(all_files), SUBPLOTS_PER_FIGURE):
            file_chunk = all_files[i:i + SUBPLOTS_PER_FIGURE]
            create_subplot_figure(file_chunk, i // SUBPLOTS_PER_FIGURE + 1)

    except FileNotFoundError:
        print(f"Error: The input directory '{input_dir}' was not found. Please check the path.")
    except Exception as e:
        print(f"An error occurred: {e}")

def create_subplot_figure(file_paths, figure_number):
    """
    Creates a single figure with subplots for each file in the list.

    Args:
        file_paths (list): A list of file paths to process.
        figure_number (int): The sequential number for the figure, used for naming.
    """
    num_plots = len(file_paths)
    rows = math.ceil(num_plots / 3) if num_plots > 3 else 1
    cols = min(num_plots, 3)

    fig, axes = plt.subplots(rows, cols, figsize=(8 * cols, 6 * rows), squeeze=False)
    fig.suptitle(f'Distribution of Genomic Region Widths - Figure {figure_number}', fontsize=20, y=1.02)
    
    # Flatten the axes array for easy iteration.
    axes = axes.flatten()

    for i, file_path in enumerate(file_paths):
        ax = axes[i]
        
        try:
            # Read the file. narrowPeak files have a different column structure.
            # NarrowPeak columns: 0:chr, 1:start, 2:end, 3:name, 4:score, 5:strand, 6:signalValue, 7:pValue, 8:qValue, 9:peak
            # For this analysis, we just need start and end, which are consistent.
            df = pd.read_csv(file_path, header=None, sep='\t')
            df['width'] = df.iloc[:, 2] - df.iloc[:, 1]
            widths = df['width']

            total_regions = len(widths)
            mean_width = widths.mean()
            median_width = widths.median()
            
            # Create the histogram on the current subplot.
            ax.hist(widths, bins=100, color='skyblue', edgecolor='black')
            
            # Add vertical lines for mean and median.
            ax.axvline(mean_width, color='red', linestyle='dashed', linewidth=1.5, label=f'Mean: {mean_width:.2f}')
            ax.axvline(median_width, color='green', linestyle='dashed', linewidth=1.5, label=f'Median: {median_width:.2f}')
            
            # Add a legend, title, and labels.
            ax.legend()
            ax.set_title(os.path.basename(file_path), fontsize=14)
            ax.set_xlabel('Region Width', fontsize=12)
            ax.set_ylabel('Frequency', fontsize=12)
            ax.grid(axis='y', alpha=0.75)

            # Add a text annotation with the summary statistics.
            ax.text(
                0.95,
                0.95,
                f'Total Regions: {total_regions}\nMean Width: {mean_width:.2f}\nMedian Width: {median_width:.2f}',
                horizontalalignment='right',
                verticalalignment='top',
                transform=ax.transAxes,
                fontsize=10,
                bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='gray', lw=1, alpha=0.8),
            )
            
        except Exception as e:
            ax.set_title(f"Error for {os.path.basename(file_path)}", fontsize=14)
            ax.text(0.5, 0.5, f"Could not process file:\n{e}",
                    ha='center', va='center', transform=ax.transAxes, color='red')
            print(f"Skipping analysis for '{file_path}' due to an error: {e}")

    # Hide any unused subplots.
    for j in range(num_plots, len(axes)):
        axes[j].axis('off')

    plt.tight_layout()

    # Sanitize the filename for saving the plot.
    results_path = os.path.join(RESULTS_DIR, f"batch_analysis_figure_{figure_number}.png")
    fig.savefig(results_path)
    print(f"Figure {figure_number} saved as '{results_path}'")
    
    plt.close(fig) # Close the figure to free up memory



# To run the script, simply call the function with the path.
if __name__ == '__main__':
    analyze_bed_files_in_directory(INPUT_DATA_DIR)