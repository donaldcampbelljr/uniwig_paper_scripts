import pandas as pd
import matplotlib.pyplot as plt
import os
import seaborn as sns
import sys


#{looper.output_dir} {sample.input} {sample.file_extension}


# Define the directory for results
#RESULTS_DIR = "/home/drc/Downloads/test_plotting_script/test2/"
RESULTS_DIR = sys.argv[1]

# Define the directory containing the BED files
#INPUT_PATH = "/home/drc/Downloads/GTARS_PAPER/sample_list/fullpath_15scatlas.txt"
INPUT_PATH = sys.argv[2]


# File extension to look for
#FILE_EXTENSION = ".gz"
FILE_EXTENSION = sys.argv[3]

def get_file_list(input_path):
    """
    Determines if the input path is a directory or a file listing absolute paths.
    Returns a list of file paths to process.
    """
    if os.path.isdir(input_path):
        print(f"Processing all '.narrowPeak' files in directory: {input_path}")
        return [os.path.join(input_path, f) for f in os.listdir(input_path) if f.endswith(FILE_EXTENSION)]
    elif os.path.isfile(input_path) and input_path.endswith('.txt'):
        print(f"Processing files from list in: {input_path}")
        with open(input_path, 'r') as f:
            # Strip whitespace and filter out empty lines
            return [line.strip() for line in f if line.strip()]
    else:
        raise ValueError("Input must be a directory path or a .txt file containing a list of absolute file paths.")


os.makedirs(RESULTS_DIR, exist_ok=True)

try:
    file_paths = get_file_list(INPUT_PATH)
except ValueError as e:
    print(e)


# Create a list to store data from all files for later DataFrame creation
all_data = []
processed_files = []

# Loop through all files in the directory
for file_path in file_paths:
    filename = os.path.basename(file_path)

    if not filename.endswith(FILE_EXTENSION): 
        print(f"Skipping {filename}: Not a {FILE_EXTENSION} file.")
        continue

    
    try:
        # Read the file into a pandas DataFrame
        df = pd.read_csv(file_path, sep='\t', header=None)
        
        # Check if the file has at least 5 columns
        if df.shape[1] >= 5:
            # Extract the 5th column (score column)
            fifth_column = pd.to_numeric(df.iloc[:, 4], errors='coerce').dropna()
            
            # Append each value with its filename to a master list
            for value in fifth_column:
                all_data.append({'filename': filename, 'score': value})
            processed_files.append(filename)
        else:
            print(f"Skipping {filename}: Not enough columns.")
    except Exception as e:
        print(f"Error reading {filename}: {e}")

# Check if we collected any data
if not all_data:
    print("No data found in any BED files. Check your directory path and file formats.")
else:
    # Convert the list of dictionaries to a pandas DataFrame
    data_df = pd.DataFrame(all_data)
    total_count = len(data_df)

    # --- Outlier Analysis and Identification ---
    print("\n--- Outlier Analysis ---")
    data_series = data_df['score']
    
    # Calculate quartiles and IQR for outlier detection
    Q1 = data_series.quantile(0.25)
    Q3 = data_series.quantile(0.75)
    IQR = Q3 - Q1
    
    # Define outlier bounds
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    # Filter out outliers
    non_outliers_df = data_df[(data_df['score'] >= lower_bound) & (data_df['score'] <= upper_bound)]
    outliers_df = data_df[(data_df['score'] < lower_bound) | (data_df['score'] > upper_bound)]
    
    outlier_count = len(outliers_df)
    non_outlier_count = len(non_outliers_df)

    # Identify and print files containing outliers
    if not outliers_df.empty:
        files_with_outliers = outliers_df['filename'].unique()
        print("\nFiles containing outliers:")
        for file in files_with_outliers:
            print(f"- {file}")
    else:
        print("\nNo outliers were found in any of the files.")
    
    print(f"\nTotal data points: {total_count}")
    print(f"Number of outliers identified: {outlier_count}")
    print(f"Number of non-outliers remaining: {non_outlier_count}")
    
    # --- Plotting the Distribution of ALL Data (Unfiltered) ---
    print("\n--- Plotting Unfiltered Data ---")
    
    plt.figure(figsize=(12, 8))
    sns.violinplot(x='filename', y='score', data=data_df, inner="quartile", palette="pastel")
    
    plt.title('Distribution of Scores per File (All Data)', fontsize=16)
    plt.xlabel('Input File', fontsize=12)
    plt.ylabel('Score Value (5th Column)', fontsize=12)
    plt.xticks(rotation=90, fontsize=8)
    plt.tight_layout()
    output_path_multi_violin = os.path.join(RESULTS_DIR, 'violin_all_files.png')
    plt.savefig(output_path_multi_violin, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Multi-violin plot saved to: {output_path_multi_violin}")


    print("\n--- Plotting Filtered Data ---")
    
    # Plot the histogram with all data
    plt.figure(figsize=(10, 6))
    data_df['score'].plot(kind='hist', bins=500, edgecolor='black', alpha=0.7, color='skyblue')
    
    plt.title(f'Distribution of Scores ALL DATA', fontsize=16)
    plt.xlabel('Score Value (5th Column)', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    mean_value = data_df['score'].mean()
    plt.axvline(mean_value, color='red', linestyle='dashed', linewidth=2, label=f'Mean: {mean_value:.2f}')
    plt.legend()
    
    plt.tight_layout()
    output_path_hist = os.path.join(RESULTS_DIR, 'histogram_alldata.png')
    plt.savefig(output_path_hist, dpi=300, bbox_inches='tight')
    plt.close()

    # --- Plotting the Filtered Data (w/o outliers) ---
    if non_outlier_count > 0:
        print("\n--- Plotting Filtered Data ---")
        
        # Plot the histogram with outliers filtered out
        plt.figure(figsize=(10, 6))
        non_outliers_df['score'].plot(kind='hist', bins=50, edgecolor='black', alpha=0.7, color='skyblue')
        
        plt.title(f'Distribution of Scores (w/o Outliers, #of outliers filtered={outlier_count}, # remaining = {non_outlier_count})', fontsize=16)
        plt.xlabel('Score Value (5th Column)', fontsize=12)
        plt.ylabel('Frequency', fontsize=12)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        mean_value = non_outliers_df['score'].mean()
        plt.axvline(mean_value, color='red', linestyle='dashed', linewidth=2, label=f'Mean: {mean_value:.2f}')
        plt.legend()
        
        plt.tight_layout()
        output_path_hist = os.path.join(RESULTS_DIR, 'histogram_nooutliers.png')
        plt.savefig(output_path_hist, dpi=300, bbox_inches='tight')
        plt.close()

        # Plot the violin plot with outliers filtered out
        plt.figure(figsize=(8, 6))
        sns.violinplot(y=non_outliers_df['score'], inner="quartile", color='lightblue')

        plt.title(f'Distribution of Scores (w/o Outliers, #of outliers filtered={outlier_count}, # remaining = {non_outlier_count})', fontsize=16)
        plt.ylabel('Score Value (5th Column)', fontsize=12)
        plt.xlabel('')
        
        plt.tight_layout()
        output_path_violin = os.path.join(RESULTS_DIR, 'violin_nooutliers.png')
        plt.savefig(output_path_violin, dpi=300, bbox_inches='tight')
        plt.close()
        
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