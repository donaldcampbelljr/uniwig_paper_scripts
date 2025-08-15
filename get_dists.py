import pandas as pd
import matplotlib.pyplot as plt
import os
import seaborn as sns

# Define the directory containing the BED files
directory_path = "/home/drc/Downloads/GTARS_PAPER/sample_list/CTCF_40/"

# Define the directory for results
RESULTS_DIR = "/home/drc/Downloads/uniwig_paper_figs/"

# Create an empty list to store all the 5th column values
all_values = []

# Loop through all files in the directory
for filename in os.listdir(directory_path):
    if filename.endswith(".bed.gz"):  # Process only .bed files
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