import os
import pypiper
import sys



#RESULTS_DIRECTORY = "/home/drc/Downloads/test_sorting/pipeline_results/"
RESULTS_DIRECTORY = sys.argv[1]

sample_name = sys.argv[2]


#INPUT_DIRECTORY = "/home/drc/Downloads/test_sorting/input/"
INPUT_DIRECTORY = sys.argv[3]

#FILE_LIST = "/home/drc/Downloads/test_sorting/input/file_list.txt" # -> needs to be absolute paths to all files used in input directory (for assessment)
FILE_LIST = sys.argv[4]

#CHROM_SIZES = "/home/drc/GITHUB/gtars/gtars/tests/hg38.chrom.sizes"
CHROM_SIZES = sys.argv[5]

#GTARS_PATH = "/home/drc/GITHUB/gtars/gtars/target/release/gtars"
GTARS_PATH = sys.argv[6]

SCORING = "ALL"




# SET UP DIRECTORIES
# UNIWIG, UNIVERSE, STATS, FIGURES, logs

LOGS_DIR = os.path.join(RESULTS_DIRECTORY, "logs", f"{sample_name}")
UNIWIG_OUTPUT = os.path.join(RESULTS_DIRECTORY, "uniwig_output", f"{sample_name}")


directories = [LOGS_DIR, UNIWIG_OUTPUT,]
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


# pre check that file list is in input directory?

# Check for files in input directory

# Check if gtars is callable
gtars_cmd_callable = ngstk.check_command(GTARS_PATH)
print(f"Can we use gtars? -> {gtars_cmd_callable}")

if not gtars_cmd_callable:
    pm.stop_pipeline()
    raise Exception

# Scored
score_output_dir = os.path.join(UNIWIG_OUTPUT, "score/")
if not os.path.exists(score_output_dir):
    os.makedirs(score_output_dir)
    print(f"Created directory: {score_output_dir}")
else:
    print(f"Directory already exists: {score_output_dir}")

gtars_scored_cmd = f"{GTARS_PATH} uniwig -f {INPUT_DIRECTORY} -c {CHROM_SIZES} -m 25 -s 1 -t bed -y bw -p 6 -l {score_output_dir}'all' -o"

# No score
no_score_output_dir = os.path.join(UNIWIG_OUTPUT, "no_score/")
if not os.path.exists(no_score_output_dir):
    os.makedirs(no_score_output_dir)
    print(f"Created directory: {no_score_output_dir}")
else:
    print(f"Directory already exists: {no_score_output_dir}")

gtars_no_score_cmd = f"{GTARS_PATH} uniwig -f {INPUT_DIRECTORY} -c {CHROM_SIZES} -m 25 -s 1 -t bed -y bw -p 6 -l {no_score_output_dir}'all'"

gtars1 = (gtars_no_score_cmd, no_score_output_dir)
gtars2 = (gtars_scored_cmd, score_output_dir)

if SCORING == "ALL":
    gtars_commands_to_run = [gtars1, gtars2]

if SCORING == "SCORED":
    gtars_commands_to_run = [gtars2]

if SCORING == "NO_SCORE":
    gtars_commands_to_run = [gtars1]


for cmd in gtars_commands_to_run:
    # if uniwig fails, may need to clear previous bedGraph results
    pm.run(cmd[0], cmd[1]+"_all")


pm.stop_pipeline()
