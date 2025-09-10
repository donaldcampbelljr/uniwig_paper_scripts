# Looks at the width of regions in bed files, to be used to evaluate differences in Universes.

import pandas as pd
import matplotlib.pyplot as plt
import os
from scipy.stats import ttest_ind

# Define the directory where the plots will be saved.
# This variable is taken from the user's previous code.
RESULTS_DIR = "/home/drc/Downloads/GTARS_PAPER/PROCESSED/stats_from_rivanna/"

def analyze_bed_file(file_path):
    """
    Reads a BED file, calculates region widths, creates a histogram,
    and displays the total number of regions, mean, and median
    on the plot.

    Args:
        file_path (str): The path to the BED file.
    """
    try:
        # Check if the results directory exists, and create it if it doesn't.
        if not os.path.exists(RESULTS_DIR):
            os.makedirs(RESULTS_DIR)

        # Read the BED file without a header and with tab separation.
        # It's assumed to have columns: chromosome, start, end, ...
        df = pd.read_csv(file_path, header=None, sep='\t')

        # Calculate the region width by subtracting the second column (start)
        # from the third column (end).
        # Assuming BED file columns are 0-indexed: 0:chromosome, 1:start, 2:end.
        df['width'] = df.iloc[:, 2] - df.iloc[:, 1]

        # Get the total number of regions.
        total_regions = len(df)

        # Calculate the mean and median of the region widths.
        mean_width = df['width'].mean()
        median_width = df['width'].median()

        # Create the histogram plot.
        plt.figure(figsize=(10, 6))
        plt.hist(df['width'], bins=50, color='skyblue', edgecolor='black')

        # Add vertical dashed lines for the mean and median.
        plt.axvline(mean_width, color='red', linestyle='dashed', linewidth=1.5, label=f'Mean: {mean_width:.2f}')
        plt.axvline(median_width, color='green', linestyle='dashed', linewidth=1.5, label=f'Median: {median_width:.2f}')
        
        # Add a legend to the plot to show the mean and median labels.
        plt.legend()

        # Add titles and labels.
        plt.title(f'Distribution of Genomic Region Widths for {os.path.basename(file_path)}', fontsize=16)
        plt.xlabel('Region Width', fontsize=12)
        plt.ylabel('Frequency', fontsize=12)
        plt.grid(axis='y', alpha=0.75)

        # Add a text annotation with the summary statistics.
        plt.text(
            0.95,
            0.95,
            f'Total Regions: {total_regions}\nMean Width: {mean_width:.2f}\nMedian Width: {median_width:.2f}',
            horizontalalignment='right',
            verticalalignment='top',
            transform=plt.gca().transAxes,
            fontsize=12,
            bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='gray', lw=1, alpha=0.8),
        )

        # Sanitize the filename for saving the plot.
        output_filename = os.path.basename(file_path).replace('.bed', '_histogram.png')
        results_path = os.path.join(RESULTS_DIR, output_filename)
        plt.savefig(results_path)

        print(f"Analysis complete. Histogram saved as '{results_path}'")
        return df['width']

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found. Please check the file path.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Define the file paths provided by the user.
bedfile1 = "/home/drc/Downloads/uniwig_outputs_Rivanna_26aug2025/scatlas/universe_output/scatlas2_03/score/hmm/hmm_score_scatlas2_03.bed"
bedfile2 = "/home/drc/Downloads/uniwig_outputs_Rivanna_26aug2025/scatlas/universe_output/scatlas2_07/no_score/hmm/hmm_no_score_scatlas2_07.bed"

bedfile3 = "/home/drc/Downloads/uniwig_outputs_Rivanna_26aug2025/lympho_sample/universe_output/lympho400_03/score/hmm/hmm_score_lympho400_03.bed"
bedfile4 = "/home/drc/Downloads/uniwig_outputs_Rivanna_26aug2025/lympho_sample/universe_output/lympho400_07/no_score/hmm/hmm_no_score_lympho400_07.bed"

bedfile5 =  "/home/drc/Downloads/uniwig_outputs_Rivanna_26aug2025/atacseq500/universe_output/atacseq500_03/score/hmm/hmm_score_atacseq500_03.bed"
bedfile6 =  "/home/drc/Downloads/uniwig_outputs_Rivanna_26aug2025/atacseq500/universe_output/atacseq500_07/no_score/hmm/hmm_no_score_atacseq500_07.bed"

# Run the analysis for both files.
widths1 = analyze_bed_file(bedfile1)
widths2 = analyze_bed_file(bedfile2)
widths3 = analyze_bed_file(bedfile3)
widths4 = analyze_bed_file(bedfile4)
widths5 = analyze_bed_file(bedfile5)
widths6 = analyze_bed_file(bedfile6)

if widths1 is not None and widths2 is not None:
    print("\nPerforming two-sample t-test to compare region width distributions...")
    try:
        t_statistic, p_value = ttest_ind(widths1, widths2, equal_var=False)

        print(f"T-statistic: {t_statistic:.6f}")
        print(f"P-value: {p_value:.6f}")
        
        # Interpret the result based on the p-value.
        alpha = 0.05
        if p_value < alpha:
            print("\nResult: The difference between the two distributions is statistically significant.")
            print("This suggests that the region widths in the two BED files are likely from different populations.")
        else:
            print("\nResult: The difference between the two distributions is not statistically significant.")
            print("This suggests that the region widths in the two BED files are likely from the same population.")
            
    except Exception as e:
        print(f"An error occurred during the t-test: {e}")