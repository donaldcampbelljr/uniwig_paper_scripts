import pandas as pd
import matplotlib.pyplot as plt
import os
import seaborn as sns

# Define the directory containing the BED files
directory_path = "/home/drc/Downloads/GTARS_PAPER/sample_list/nathan_scatlas_macs2_narrowpeaks/"

# Define the directory for results
RESULTS_DIR = "/home/drc/Downloads/uniwig_paper_figs/15_scatlas2_narrowpeaks/"

# Create an empty list to store all the 5th column values
all_values = []

# Loop through all files in the directory
for filename in os.listdir(directory_path):
    if filename.endswith(".narrowPeak"):  # Process only .bed files
        file_path = os.path.join(directory_path, filename)
        
        # Read the BED file into a pandas DataFrame
        # The 5th column is at index 4 (0-based)
        # Use sep='\t' since BED files are usually tab-separated
        try:
            df = pd.read_csv(file_path, sep='\t', header=None)
            
            # Check if the file has at least 5 columns
            if df.shape[1] >= 5:
                # Extract the 5th column (score column)
                fifth_column = df.iloc[:, 4]
                
                # Append the values to our list, converting to numeric if needed
                all_values.extend(pd.to_numeric(fifth_column, errors='coerce').dropna())
            else:
                print(f"Skipping {filename}: Not enough columns.")
        except Exception as e:
            print(f"Error reading {filename}: {e}")

# Check if we collected any data
if not all_values:
    print("No data found in any BED files. Check your directory path and file formats.")
else:
    # Create a pandas Series from the collected values for easier plotting
    data_series = pd.Series(all_values)

    # Plot the distribution
    plt.figure(figsize=(10, 6))
    data_series.plot(kind='hist', bins=50, edgecolor='black', alpha=0.7, color='skyblue')
    
    # Add titles and labels for clarity
    plt.title('Distribution of Scores from BED Files', fontsize=16)
    plt.xlabel('Score Value (5th Column)', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Add a vertical line for the mean to provide additional context
    mean_value = data_series.mean()
    plt.axvline(mean_value, color='red', linestyle='dashed', linewidth=2, label=f'Mean: {mean_value:.2f}')
    plt.legend()

    # Display the plot
    plt.tight_layout()
    #plt.show()
    output_path = os.path.join(RESULTS_DIR, f'histogram.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

    
    
    # Plot the data using a violin plot
    plt.figure(figsize=(8, 6))
    
    # seaborn requires a DataFrame or Series, so we convert the list
    sns.violinplot(y=all_values, inner="quartile", color='lightblue')

    # Add titles and labels for clarity
    plt.title('Distribution of Scores using a Violin Plot', fontsize=16)
    plt.ylabel('Score Value (5th Column)', fontsize=12)
    plt.xlabel('') # No x-label needed for a single plot
    
    # Display the plot
    plt.tight_layout()
    #plt.show()
    output_path = os.path.join(RESULTS_DIR, f'violin.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()


if not all_values:
    print("No data found in any BED files. Check your directory path and file formats.")
else:
    # Convert to a pandas Series for easy calculation of quartiles
    data_series = pd.Series(all_values)
    total_count = len(data_series)

    print(f"Minimum Value before filtering: {data_series.min()}")
    print(f"Maximum Value before filtering: {data_series.max()}")
    
    # Calculate quartiles and IQR for outlier detection
    Q1 = data_series.quantile(0.25)
    Q3 = data_series.quantile(0.75)
    IQR = Q3 - Q1
    
    # Define outlier bounds
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    # Filter out outliers
    non_outliers = data_series[(data_series >= lower_bound) & (data_series <= upper_bound)]
    outliers = data_series[(data_series < lower_bound) | (data_series > upper_bound)]
    
    non_outlier_count = len(non_outliers)
    outlier_count = len(outliers)

    print(f"Minimum Value after filtering: {non_outliers.min()}")
    print(f"Maximum Value after filtering: {non_outliers.max()}")

    # Handle the case where all values are outliers
    if non_outlier_count == 0:
        print("All data points were identified as outliers. No data to plot after filtering.")
    else:
        # Plot the histogram with outliers filtered out
        plt.figure(figsize=(10, 6))
        non_outliers.plot(kind='hist', bins=50, edgecolor='black', alpha=0.7, color='skyblue')
        
        plt.title(f'Distribution of Scores (w/o Outliers, #of outliers filtered={outlier_count}, # remaining = {non_outlier_count})', fontsize=16)
        plt.xlabel('Score Value (5th Column)', fontsize=12)
        plt.ylabel('Frequency', fontsize=12)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        mean_value = non_outliers.mean()
        plt.axvline(mean_value, color='red', linestyle='dashed', linewidth=2, label=f'Mean: {mean_value:.2f}')
        plt.legend()
        
        plt.tight_layout()
        output_path_hist = os.path.join(RESULTS_DIR, 'histogram_nooutliers.png')
        plt.savefig(output_path_hist, dpi=300, bbox_inches='tight')
        plt.close()

        # Plot the violin plot with outliers filtered out
        plt.figure(figsize=(8, 6))
        sns.violinplot(y=non_outliers, inner="quartile", color='lightblue')

        plt.title(f'Distribution of Scores (w/o Outliers, #of outliers filtered={outlier_count}, # remaining = {non_outlier_count})', fontsize=16)
        plt.ylabel('Score Value (5th Column)', fontsize=12)
        plt.xlabel('')
        
        plt.tight_layout()
        output_path_violin = os.path.join(RESULTS_DIR, 'violin_nooutliers.png')
        plt.savefig(output_path_violin, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"Total data points found: {total_count}")
        print(f"Number of outliers identified: {outlier_count}")
        print(f"Number of non-outliers remaining: {non_outlier_count}")
        print(f"Histogram saved to: {output_path_hist}")
        print(f"Violin plot saved to: {output_path_violin}")

# # Check if we collected any data
# if not all_values:
#     print("No data found in any BED files. Check your directory path and file formats.")
# else:
#     # Filter out zero values for both plots as requested
#     non_zero_values = [value for value in all_values if value != 0]
#     total_count = len(non_zero_values)
    
#     # Handle the case where all values are zero
#     if total_count == 0:
#         print("No non-zero data points to plot.")
#     else:
#         # Convert to a pandas Series for plotting
#         data_series = pd.Series(non_zero_values)

#         # Plot the histogram
#         plt.figure(figsize=(10, 6))
#         data_series.plot(kind='hist', bins=50, edgecolor='black', alpha=0.7, color='skyblue')
        
#         plt.title(f'Distribution of Scores (n={total_count})', fontsize=16)
#         plt.xlabel('Score Value (5th Column)', fontsize=12)
#         plt.ylabel('Frequency', fontsize=12)
#         plt.grid(axis='y', linestyle='--', alpha=0.7)
        
#         mean_value = data_series.mean()
#         plt.axvline(mean_value, color='red', linestyle='dashed', linewidth=2, label=f'Mean: {mean_value:.2f}')
#         plt.legend()
        
#         plt.tight_layout()
#         output_path_hist = os.path.join(RESULTS_DIR, 'histogram_nozero.png')
#         plt.savefig(output_path_hist, dpi=300, bbox_inches='tight')
#         plt.close()

#         # Plot the violin plot
#         plt.figure(figsize=(8, 6))
#         sns.violinplot(y=non_zero_values, inner="quartile", color='lightblue')

#         plt.title(f'Distribution of Scores (n={total_count})', fontsize=16)
#         plt.ylabel('Score Value (5th Column)', fontsize=12)
#         plt.xlabel('')
        
#         plt.tight_layout()
#         output_path_violin = os.path.join(RESULTS_DIR, 'violin_nozero.png')
#         plt.savefig(output_path_violin, dpi=300, bbox_inches='tight')
#         plt.close()
        
#         print(f"Total non-zero data points found: {total_count}")
#         print(f"Histogram saved to: {output_path_hist}")
#         print(f"Violin plot saved to: {output_path_violin}")