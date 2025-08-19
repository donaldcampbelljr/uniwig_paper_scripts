import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os
from utils import f_beta_score


# WHICH GRAPHS DO YOU WANT TO PRODUCE

GROUPED_BAR_GRAPH = True
BOX_PLOT = True


# Define the directory for results
RESULTS_DIR = "/home/drc/Downloads/uniwig_paper_figs/"

# File paths for all four data sources
cc_scored_data = "/home/drc/Downloads/GTARS_PAPER/PROCESSED/STATS/scored_stats/cc_scored_data.csv"
cc_no_scored_data = "/home/drc/Downloads/GTARS_PAPER/PROCESSED/STATS/no_score_stats/cc_no_score_data.csv"
cc_new_score = "/home/drc/Downloads/GTARS_PAPER/PROCESSED/STATS/scored_stats/cc_NEW_score_data.csv"

ccf_scored_data = "/home/drc/Downloads/GTARS_PAPER/PROCESSED/STATS/scored_stats/ccf_scored_data.csv"
ccf_no_score_data = "/home/drc/Downloads/GTARS_PAPER/PROCESSED/STATS/no_score_stats/ccf_no_score_data.csv"
ccf_new_score = "/home/drc/Downloads/GTARS_PAPER/PROCESSED/STATS/scored_stats/ccf_NEW_score_data.csv"

hmm_scored_data = "/home/drc/Downloads/GTARS_PAPER/PROCESSED/STATS/scored_stats/hmm_scored_data.csv"
hmm_no_score_data = "/home/drc/Downloads/GTARS_PAPER/PROCESSED/STATS/no_score_stats/hmm_no_score_data.csv"
hmm_new_score = "/home/drc/Downloads/GTARS_PAPER/PROCESSED/STATS/scored_stats/hmm_NEW_score_data.csv"

ml_scored_data = "/home/drc/Downloads/GTARS_PAPER/PROCESSED/STATS/scored_stats/ml_score_data.csv"
ml_new_score = "/home/drc/Downloads/GTARS_PAPER/PROCESSED/STATS/scored_stats/ml_NEW_score_data.csv"
ml_no_score = "/home/drc/Downloads/GTARS_PAPER/PROCESSED/STATS/no_score_stats/ml_no_score_data.csv"

# Read the data from all four CSV files
df_cc_score = pd.read_csv(cc_scored_data)
df_cc_no_score = pd.read_csv(cc_no_scored_data)
df_cc_new_score = pd.read_csv(cc_new_score)

df_ccf_score = pd.read_csv(ccf_scored_data)
df_ccf_no_score = pd.read_csv(ccf_no_score_data)
df_ccf_new_score = pd.read_csv(ccf_new_score)

df_hmm_score  = pd.read_csv(hmm_scored_data)
df_hmm_no_score  = pd.read_csv(hmm_no_score_data)
df_hmm_new_score = pd.read_csv(hmm_new_score)

df_ml_score = pd.read_csv(ml_scored_data)
df_ml_no_score  = pd.read_csv(ml_no_score)
df_ml_new_score = pd.read_csv(ml_new_score)

# Define the column name for the statistic you want to plot

stats = ["median_dist_file_to_universe", 'univers/file', 'file/universe', 'universe&file', 'f10_beta_score']

# Add a 'data_source' column to each DataFrame to differentiate them
df_cc_score['data_source'] = 'CC_old'
df_cc_no_score['data_source'] = 'CC_no_score'
df_cc_new_score['data_source'] = 'CC_new'

df_ccf_score['data_source'] = 'CCF_old'
df_ccf_no_score['data_source'] = 'CCF_no_score'
df_ccf_new_score['data_source'] = 'CCF_new'

df_hmm_score['data_source'] = 'HMM_old'
df_hmm_no_score['data_source'] = 'HMM_no_score'
df_hmm_new_score['data_source'] = 'HMM_new'

df_ml_score['data_source'] = 'ML_old'
df_ml_no_score['data_source'] = 'ML_no_score'
df_ml_new_score['data_source'] = 'ML_new'

df_combined = pd.concat([df_cc_score, df_cc_new_score, df_cc_no_score, df_ccf_score,df_ccf_new_score,df_ccf_no_score, df_hmm_score,df_hmm_new_score,df_hmm_no_score,df_ml_score,df_ml_new_score,df_ml_no_score])

#df_combined = pd.concat([df_ccf_score, df_ccf_new_score, df_ccf_no_score])
#df_combined = pd.concat([df_cc_score, df_cc_new_score, df_cc_no_score])
#df_combined = pd.concat([df_hmm_score,df_hmm_new_score,df_hmm_no_score])

df_combined.dropna(inplace=True) # ccf_new has a few NaNs in median_dist column

# From Reading the Paper
# univers only - "univers/file" = FP
# "file/universe" - query only = FN
# overlap = TP

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
    for stat in stats:
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
        #plt.show()
        # Save the heatmap plot
        stat_rename = stat.replace('/', '_')
        output_path = os.path.join(RESULTS_DIR, f'{stat_rename}_comparison.png') # New filename
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()


if BOX_PLOT:
    for stat in stats:
        # Create the box plot using seaborn, grouping by data_source
        plt.figure(figsize=(12, 8))
        sns.boxplot(x='data_source', y=stat, data=df_combined, palette='viridis')

        # Add titles and labels for clarity
        plt.title(f'Box Plot of {stat} Grouped by Data Source', fontsize=16)
        plt.xlabel('Data Source', fontsize=12)
        plt.ylabel(f'{stat}', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y', linestyle='--')
        plt.tight_layout()

        # Save the plot
        stat_rename = stat.replace('/', '_')
        output_path = os.path.join(RESULTS_DIR, f'{stat_rename}_boxplot_comparison.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
