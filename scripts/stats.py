import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os
from utils import f_beta_score

# WHICH GRAPHS DO YOU WANT TO PRODUCE
GROUPED_BAR_GRAPH = False
BOX_PLOT = True

# Define the directory for results and the input data
RESULTS_DIR = "/home/drc/Downloads/GTARS_PAPER/PROCESSED/stats_from_rivanna/lympho400/FIGS/"
DATA_DIR = "/home/drc/Downloads/GTARS_PAPER/PROCESSED/stats_from_rivanna/lympho400/stats_output/"


# Ensure the results directory exists
if not os.path.exists(RESULTS_DIR):
    os.makedirs(RESULTS_DIR)

# Define the column names for the statistics you want to plot
stats = ["median_dist_file_to_universe", 'univers/file', 'file/universe', 'universe&file', 'f10_beta_score']

# List to hold all dataframes
list_of_dfs = []

# # Process scored data

# for filename in sorted(os.listdir(DATA_DIR)):
#     if filename.endswith(".csv"):
#         file_path = os.path.join(DATA_DIR, filename)
#         df = pd.read_csv(file_path)
#         base_name = filename.split('.')[0].upper()
#         print(f"Here is basename {base_name}")
#         df['data_source'] = f"{base_name}"
#         list_of_dfs.append(df)

for root, dirs, files in os.walk(DATA_DIR):
    for filename in sorted(files):
        if filename.endswith(".csv"):
            file_path = os.path.join(root, filename)
            df = pd.read_csv(file_path)
            
            # The base name is the name of the file without the extension
            base_name = os.path.splitext(filename)[0].upper()
            
            print(f"Here is basename {base_name}")
            
            # Add a 'data_source' column to the DataFrame
            df['data_source'] = f"{base_name}"
            
            list_of_dfs.append(df)

# Combine all the dataframes into a single dataframe
if not list_of_dfs:
    print("No CSV files found. Please check the directory paths.")
else:
    df_combined = pd.concat(list_of_dfs, ignore_index=True)
    df_combined.dropna(inplace=True)

    # Re-calculate the F-beta score for all combined data
    beta_value = 10
    df_combined['f10_beta_score'] = df_combined.apply(
        lambda row: f_beta_score(
            beta_value,
            tp=row['universe&file'],
            fp=row['univers/file'],
            fn=row['file/universe']
        ),
        axis=1
    )

    if GROUPED_BAR_GRAPH:
        print("Generating grouped bar graphs...")
        for stat in stats:
            plt.figure(figsize=(12, 8))
            sns.barplot(x='file', y=stat, hue='data_source', data=df_combined, palette='viridis')
            plt.title(f'Grouped Bar Plot of {stat} for All Data Sources', fontsize=16)
            plt.xlabel('File', fontsize=12)
            plt.ylabel(f'{stat}', fontsize=12)
            plt.xticks(rotation=45, ha='right')
            plt.legend(title='Data Source')
            plt.grid(axis='y', linestyle='--')
            plt.tight_layout()
            
            stat_rename = stat.replace('/', '_')
            output_path = os.path.join(RESULTS_DIR, f'{stat_rename}_comparison.png')
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close()
        print("Grouped bar graphs saved.")

    if BOX_PLOT:
        print("Generating box plots...")
        for stat in stats:
            plt.figure(figsize=(12, 8))
            sns.boxplot(x='data_source', y=stat, data=df_combined, palette='viridis')
            plt.title(f'Box Plot of {stat} Grouped by Data Source', fontsize=16)
            plt.xlabel('Data Source', fontsize=12)
            plt.ylabel(f'{stat}', fontsize=12)
            plt.xticks(rotation=45, ha='right')
            plt.grid(axis='y', linestyle='--')
            plt.tight_layout()
            
            stat_rename = stat.replace('/', '_')
            output_path = os.path.join(RESULTS_DIR, f'{stat_rename}_boxplot_comparison.png')
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close()
        print("Box plots saved.")