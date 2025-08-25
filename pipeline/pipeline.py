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
UNIVERSES = ["cc", "ccf", "hmm", "ml"]



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


# CHECK OUTPUT
required_files = ['all_core.bw', 'all_start.bw', 'all_end.bw']
for cmd in gtars_commands_to_run:
    directory = cmd[1]
    for filename in required_files:
        filepath = os.path.join(directory, filename)
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Missing required file: {filepath}")
    print(f"All required files found in directory: {directory}")


# Now for each score vs no score, create universes
# Check if gtars is callable
geniml_cmd_callable = ngstk.check_command("geniml")
print(f"Can we use geniml? -> {geniml_cmd_callable}")

if not geniml_cmd_callable:
    pm.stop_pipeline()
    raise Exception


# scoring = []
# if SCORING == "ALL":
#     scoring=["scored","no_score]"

# if SCORING == "SCORED":
#     commands_to_run = [gtars2]

# if SCORING == "NO_SCORE":
#     commands_to_run = [gtars1]

universe_commands = []
for cmd in gtars_commands_to_run:
    # get score and no score
    score_dirname = os.path.basename(os.path.dirname(cmd[1]))
    coverage_folder = cmd[1]
    print(score_dirname)
    for universe in UNIVERSES:
        if universe == "ml":
            continue #requires extra step
        output_dir = os.path.join(UNIVERSE_OUTPUT, score_dirname,universe)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"Created directory: {output_dir}")
        else:
            print(f"Directory already exists: {output_dir}")
        subcommand = universe
        target_file =  os.path.join(output_dir,f"{universe}_{score_dirname}_{sample_name}.bed")
        geniml_cmd  = f"geniml build-universe {subcommand} --output-file {target_file} --coverage-folder {coverage_folder}"
        universe_commands.append((geniml_cmd, target_file, score_dirname, universe))

for universe_cmd in universe_commands:
    pm.run(universe_cmd[0], universe_cmd[1])


# Asess each universe
assess_commands = []

for uc in universe_commands:
    output_dir = os.path.join(STATS_OUTPUT, uc[2], uc[3])
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")
    else:
        print(f"Directory already exists: {output_dir}")
    prefix = f"{uc[3]}_{uc[2]}_{sample_name}"
    target = prefix+"_data.csv"
    assess_command = f"geniml assess-universe --overlap --distance --distance-universe-to-file --universe {uc[1]} --raw-data-folder {INPUT_DIRECTORY} --folder-out {output_dir} --save-to-file --file-list {FILE_LIST} --pref {prefix}"
    assess_commands.append((assess_command, target))

for assess_cmd in assess_commands:
    pm.run(assess_cmd[0], assess_cmd[1])

pm.stop_pipeline()
