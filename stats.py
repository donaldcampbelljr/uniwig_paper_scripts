import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Define the directory for results
RESULTS_DIR = "/home/drc/Downloads/uniwig_paper_figs/"

# File paths for all four data sources
cc_scored_data = "/home/drc/Downloads/GTARS_PAPER/PROCESSED/STATS/scored_stats/cc_scored_data.csv"
cc_no_scored_data = "/home/drc/Downloads/GTARS_PAPER/PROCESSED/STATS/no_score_stats/cc_no_score_data.csv"

ccf_scored_data = "/home/drc/Downloads/GTARS_PAPER/PROCESSED/STATS/scored_stats/ccf_scored_data.csv"
ccf_no_score_data = "/home/drc/Downloads/GTARS_PAPER/PROCESSED/STATS/no_score_stats/ccf_no_score_data.csv"

hmm_scored_data = "/home/drc/Downloads/GTARS_PAPER/PROCESSED/STATS/scored_stats/hmm_scored_data.csv"
hmm_no_score_data = "/home/drc/Downloads/GTARS_PAPER/PROCESSED/STATS/no_score_stats/hmm_no_score_data.csv"

# Read the data from all four CSV files
df_cc_score = pd.read_csv(cc_scored_data)
df_cc_no_score = pd.read_csv(cc_no_scored_data)
df_ccf_score = pd.read_csv(ccf_scored_data)
df_ccf_no_score = pd.read_csv(ccf_no_score_data)

df_hmm_score  = pd.read_csv(hmm_scored_data)
df_hmm_no_score  = pd.read_csv(hmm_no_score_data)

# Define the column name for the statistic you want to plot
stat = "median_dist_file_to_universe"

# Add a 'data_source' column to each DataFrame to differentiate them
df_cc_score['data_source'] = 'cc_scored'
df_cc_no_score['data_source'] = 'cc_no_score'
df_ccf_score['data_source'] = 'ccf_scored'
df_ccf_no_score['data_source'] = 'ccf_no_score'
df_hmm_score['data_source'] = 'hmm_scored'
df_hmm_no_score['data_source'] = 'hmm_no_score'

# Concatenate all four DataFrames into a single one
#df_combined = pd.concat([df_cc_score, df_cc_no_score, df_ccf_score, df_ccf_no_score])
df_combined = pd.concat([df_cc_score, df_ccf_score, df_hmm_score, df_cc_no_score, df_ccf_no_score, df_hmm_no_score])

# Create the grouped bar plot using seaborn
# The x-axis is 'file', the y-axis is the 'stat', and the hue groups by 'data_source'
plt.figure(figsize=(12, 8))
sns.barplot(x='file', y=stat, hue='data_source', data=df_combined, palette='viridis')

# Add titles and labels for clarity
plt.title(f'Grouped Bar Plot of {stat} for All Data Sources', fontsize=16)
plt.xlabel('File', fontsize=12)
plt.ylabel(f'{stat}', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.legend(title='Data Source')
plt.grid(axis='y', linestyle='--')
plt.tight_layout()

# Display the plot
plt.show()