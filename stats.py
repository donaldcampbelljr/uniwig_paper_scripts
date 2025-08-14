
# import pandas as pd
# import seaborn as sns
# import matplotlib.pyplot as plt
# import numpy as np

# # Create plots comparing median distances of files to universe.

# cc_scored_data="/home/drc/Downloads/GTARS_PAPER/PROCESSED/STATS/scored_stats/cc_scored_data.csv"
# cc_no_scored_data = "/home/drc/Downloads/GTARS_PAPER/PROCESSED/STATS/no_score_stats/cc_no_score_data.csv"

# df_cc_score = pd.read_csv(cc_scored_data)
# df_cc_no_score = pd.read_csv(cc_no_scored_data)

# #basic histogram

# stat = "median_dist_file_to_universe"
# #df1_new = df1.assign(Employee_Salary=df2['Salary'])

# # df_cc_score[stat] = pd.to_numeric(df_cc_score[stat], errors='coerce')
# # df_cc_no_score[stat] = pd.to_numeric(df_cc_no_score[stat], errors='coerce')

# sns.barplot(x='file', y=stat, data=df_cc_score)
# plt.title('Basic Bar Plot')
# plt.show()

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


RESULTS_DIR = "/home/drc/Downloads/uniwig_paper_figs/"

# File paths from your original code
cc_scored_data = "/home/drc/Downloads/GTARS_PAPER/PROCESSED/STATS/scored_stats/cc_scored_data.csv"
cc_no_scored_data = "/home/drc/Downloads/GTARS_PAPER/PROCESSED/STATS/no_score_stats/cc_no_score_data.csv"

ccf_scored_data = "/home/drc/Downloads/GTARS_PAPER/PROCESSED/STATS/scored_stats/ccf_scored_data.csv"
ccf_no_score_data = "/home/drc/Downloads/GTARS_PAPER/PROCESSED/STATS/no_score_stats/ccf_no_score_data.csv"

# Read the data from the CSV files
df_cc_score = pd.read_csv(cc_scored_data)
df_cc_no_score = pd.read_csv(cc_no_scored_data)

# Define the column name for the statistic you want to plot
stat = "median_dist_file_to_universe"

# Add a 'type' column to each DataFrame to differentiate the data source
df_cc_score['type'] = 'scored'
df_cc_no_score['type'] = 'no_score'

# Concatenate the two DataFrames into a single one
df_combined = pd.concat([df_cc_score, df_cc_no_score])
print(df_combined)
# Pivot the table to have 'file' as index and 'type' as columns
# The values will be the 'median_dist_file_to_universe'
df_pivoted = df_combined.pivot(index='file', columns='type', values=stat)
print(df_pivoted)

# Get the scored and no_scored values for plotting
scored_values = df_pivoted['scored']
no_scored_values = df_pivoted['no_score']
files = df_pivoted.index

# Create the stacked bar plot
plt.figure(figsize=(10, 7))
bar_width = 0.5

# Plot the 'no_score' bars first, at the bottom of the stack
plt.bar(files, no_scored_values, color='skyblue', label='No Score', width=bar_width)

# Plot the 'scored' bars on top of the 'no_score' bars
plt.bar(files, scored_values, bottom=no_scored_values, color='salmon', label='Scored', width=bar_width)

# Add titles and labels for clarity
plt.title(f'Stacked Bar Plot of {stat}', fontsize=16)
plt.xlabel('File', fontsize=12)
plt.ylabel(f'{stat}', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.legend(title='Data Type')
plt.grid(axis='y', linestyle='--')
plt.tight_layout()

# Display the plot
plt.show()
