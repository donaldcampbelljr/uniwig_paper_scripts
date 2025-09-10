# plots and compares distributions of stats for each universe, score vs no scoreimport os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import argparse
import os

def process_and_plot_pair(score_file_path, no_score_file_path, group_name, sample_name, output_dir, stat):
    """
    Loads a pair of score and no_score CSV files, plots their distributions,
    and plots the distribution of their difference.
    
    Args:
        score_file_path (str): The full path to the score file.
        no_score_file_path (str): The full path to the no_score file.
        group_name (str): The group identifier (e.g., 'cc', 'ccf', 'hmm').
        sample_name (str): The sample identifier (e.g., 'atacseq500_01').
        output_dir (str): The directory to save the output plots.
    """
    print(f'Processing pair: {group_name} {sample_name}')
    
    print(f"Score path: {score_file_path}")
    print(f"No score path: {no_score_file_path}")

    

    try:
        # Load the data
        df_score = pd.read_csv(score_file_path)
        df_no_score = pd.read_csv(no_score_file_path)
        
        # Ensure the required column exists
        if stat not in df_score.columns or \
           stat not in df_no_score.columns:
            print(f"Skipping pair: '{group_name}_{sample_name}' - required column missing: {stat}.")
            return

        # Get the columns to plot
        score_data = df_score[stat]
        no_score_data = df_no_score[stat]
        
        # Plot 1: Both distributions on one plot
        plt.figure(figsize=(12, 8))
        sns.histplot(score_data, kde=True, label='Score', color='royalblue', stat='density', alpha=0.6)
        sns.histplot(no_score_data, kde=True, label='No Score', color='darkorange', stat='density', alpha=0.6)
        plt.title(f'Distribution of {stat}\nfor {group_name} {sample_name}', fontsize=16, pad=20)
        plt.xlabel('Median Distance File to Universe', fontsize=12)
        plt.ylabel('Density', fontsize=12)
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f'{group_name}_{sample_name}_{stat}_distributions.png'))
        plt.close()
        
        # Plot 2: Distribution of the difference
        difference_data = score_data - no_score_data
        
        plt.figure(figsize=(12, 8))
        sns.histplot(difference_data, kde=True, color='forestgreen', stat='density')
        plt.title(f'Distribution of the Difference (Score - No Score)\nfor {group_name} {sample_name}', fontsize=16, pad=20)
        plt.xlabel('Difference in Median Distance', fontsize=12)
        plt.ylabel('Density', fontsize=12)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f'{group_name}_{sample_name}_{stat}_difference_distribution.png'))
        plt.close()

        print(f"Successfully created plots for '{group_name}_{sample_name}'.")

    except Exception as e:
        print(f"An error occurred while processing '{group_name}_{sample_name}': {e}")

def main(input_dir, output_dir, stat='median_dist_file_to_universe'):
    """
    Finds pairs of score/no_score files and orchestrates the plotting process.
    
    Args:
        input_dir (str): The root directory containing the data files.
        output_dir (str): The directory to save the generated plots.
    """
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Dictionary to store file paths for each pair
    file_pairs = {}
    
    # Walk through the input directory and its subdirectories
    for dirpath, _, filenames in os.walk(input_dir):
        for filename in filenames:
            if filename.endswith('.csv'):
                # Split the filename to identify group, score type, and sample name
                

                if '_no_score_' in filename:
                    parts = filename.replace('.csv', '').split('_no_score_')
                    group_name = parts[0]
                    score_type = 'no_score'
                    sample_name = parts[1].split('_')[0]
                elif '_score_' in filename:
                    parts = filename.replace('.csv', '').split('_score_')
                    group_name = parts[0]
                    score_type = 'score'
                    sample_name = parts[1].split('_')[0]
                    
                else:
                    continue # Skip files that don't match the pattern

                # Create a unique key for each pair
                pair_key = f'{group_name}_{sample_name}'

                print(f"{filename} {score_type} {pair_key}")

                if pair_key not in file_pairs:
                    file_pairs[pair_key] = {}
                
                if score_type in ['score', 'no_score']:
                    file_pairs[pair_key][score_type] = os.path.join(dirpath, filename)
    
    # Process each identified pair
    processed_count = 0
    for key, file_paths in file_pairs.items():
        if 'score' in file_paths and 'no_score' in file_paths:
            group_name, sample_name = key.split('_', 1)
            process_and_plot_pair(
                file_paths['score'], 
                file_paths['no_score'], 
                group_name, 
                sample_name, 
                output_dir,
                stat
            )
            processed_count += 1
        else:
            print(f'Incomplete pair found for key: {key}. Skipping.')
            
    if processed_count == 0:
        print("No complete pairs of 'score' and 'no_score' files were found.")

if __name__ == '__main__':
    # # Use argparse to handle command-line arguments
    # parser = argparse.ArgumentParser(description='Process pairs of score/no_score CSV files and generate plots.')
    # parser.add_argument('input_dir', type=str, help='Path to the input directory containing the data files.')
    # parser.add_argument('output_dir', type=str, help='Path to the output directory to save the plots.')
    
    # args = parser.parse_args()
    
    # # Call the main function with the provided arguments
    # main(args.input_dir, args.output_dir)
    main("/home/drc/Downloads/GTARS_PAPER/PROCESSED/UNIWIG_EXPERIMENTAL_RESULTS_RIVANNA_26Aug2025/stats_from_rivanna/atacseq500/stats_output/",
         "/home/drc/Downloads/GTARS_PAPER/ASSESSING_DISTRIBUTIONS/10sep2025/",
         stat='median_dist_file_to_universe')