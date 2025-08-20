import os
import pypiper


sample_name = "TEST"


INPUT_DIRECTORY = "/home/drc/Downloads/GTARS_PAPER/sample_list/nathan_scatlas_macs2_narrowpeaks/"
CHROM_SIZES = "/home/drc/GITHUB/gtars/gtars/tests/hg38.chrom.sizes"

RESULTS_DIRECTORY = "/home/drc/Downloads/uniwig_pipeline_test/"

GTARS_PATH = "/home/drc/GITHUB/gtars/gtars/target/release/gtars"



# SET UP DIRECTORIES
# UNIWIG, UNIVERSE, STATS, FIGURES, logs

LOGS_DIR = os.path.join(RESULTS_DIRECTORY, "logs", f"{sample_name}")
UNIWIG_OUTPUT = os.path.join(RESULTS_DIRECTORY, "uniwig_output", f"{sample_name}")
UNIVERSE_OUTPUT = os.path.join(RESULTS_DIRECTORY, "universe_output", f"{sample_name}")
STATS_OUTPUT = os.path.join(RESULTS_DIRECTORY, "stats_output", f"{sample_name}")
FIGURES_OUTPUT = os.path.join(RESULTS_DIRECTORY, "figures_output", f"{sample_name}")

directories = [LOGS_DIR, UNIWIG_OUTPUT, UNIVERSE_OUTPUT, STATS_OUTPUT, FIGURES_OUTPUT]
for dir in directories:
    if not os.path.exists(dir):
        os.makedirs(dir)
        print(f"Created directory: {dir}")
    else:
        print(f"Directory already exists: {dir}")


pm = pypiper.PipelineManager(
    name=f"uniwig_pipeline_{sample_name}",
    outfolder=LOGS_DIR,
    recover=True,
)
ngstk = pypiper.NGSTk(pm=pm)

pm.start_pipeline()


# Check for files in input directory

# Check if gtars is callable
gtars_cmd_callable = ngstk.check_command(GTARS_PATH)
print(f"Can we use gtars? -> {gtars_cmd_callable}")

if not gtars_cmd_callable:
    pm.stop_pipeline()
    raise Exception

# Scored
score_output_dir = os.path.join(UNIWIG_OUTPUT, "score")
if not os.path.exists(score_output_dir):
    os.makedirs(score_output_dir)
    print(f"Created directory: {score_output_dir}")
else:
    print(f"Directory already exists: {score_output_dir}")

gtars_scored_cmd = f"uniwig -f {INPUT_DIRECTORY} -c {CHROM_SIZES} -m 25 -s 1 -t bed -y bw -p 6 -l {score_output_dir} -o"

# No score
no_score_output_dir = os.path.join(UNIWIG_OUTPUT, "scored")
if not os.path.exists(no_score_output_dir):
    os.makedirs(no_score_output_dir)
    print(f"Created directory: {no_score_output_dir}")
else:
    print(f"Directory already exists: {no_score_output_dir}")

gtars_no_score_cmd = f"uniwig -f {INPUT_DIRECTORY} -c {CHROM_SIZES} -m 25 -s 1 -t bed -y bw -p 6 -l {no_score_output_dir} -o"


pm.stop_pipeline()
# Confirm directory of files -> each directory of files is its own experiment
# and each directory will be a sample in a PEP

# Use gtars uniwig to create bigwigs

# Build 4 different universes

# Run assessments on four different universes

# Gathers all of the stats.csv