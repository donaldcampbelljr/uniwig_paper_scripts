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

COVERAGE_FOLDER = sys.argv[7]

SCORE = sys.argv[8]

UNIVERSE = sys.argv[9]


# SET UP DIRECTORIES
# UNIWIG, UNIVERSE, STATS, FIGURES, logs

LOGS_DIR = os.path.join(RESULTS_DIRECTORY, "logs", f"{sample_name}",  f"{SCORE}", f"{UNIVERSE}")
UNIVERSE_OUTPUT = os.path.join(RESULTS_DIRECTORY, "universe_output", f"{sample_name}",  f"{SCORE}", f"{UNIVERSE}")
STATS_OUTPUT = os.path.join(RESULTS_DIRECTORY, "stats_output", f"{sample_name}",  f"{SCORE}", f"{UNIVERSE}")

directories = [LOGS_DIR, UNIVERSE_OUTPUT, STATS_OUTPUT,]
for dir in directories:
    if not os.path.exists(dir):
        os.makedirs(dir)
        print(f"Created directory: {dir}")
    else:
        print(f"Directory already exists: {dir}")

pm = pypiper.PipelineManager(
    name=f"uniwig_pipeline_{sample_name}_{SCORE}_{UNIVERSE}",
    outfolder=LOGS_DIR,
    recover=True,
)
ngstk = pypiper.NGSTk(pm=pm)

pm.start_pipeline()



# CHECK IF COVERAGE FOLDER CONTAINS UNIWIG FILES
required_files = [
    'all_core.bw',
    'all_end.bw',
    'all_start.bw'
]


missing_files = []
for filename in required_files:
    file_path = os.path.join(COVERAGE_FOLDER, filename)
    if not os.path.exists(file_path):
        missing_files.append(filename)

if missing_files:
    raise FileNotFoundError(f"The following required files are missing from the folder: {', '.join(missing_files)} \n Did you run gtars uniwig successfully in prior step?")


# CHECK IG GENIML IS CALLABLE BY PIPELINE
geniml_cmd_callable = ngstk.check_command("geniml")
print(f"Can we use geniml? -> {geniml_cmd_callable}")

if not geniml_cmd_callable:
    pm.stop_pipeline()
    raise Exception

# BUILD GENIML UNIVERSE CREATION CMD
subcommand = UNIVERSE
universe_target_file =  os.path.join(UNIVERSE_OUTPUT,f"{UNIVERSE}_{SCORE}_{sample_name}.bed")
geniml_cmd  = f"geniml build-universe {subcommand} --output-file {universe_target_file} --coverage-folder {COVERAGE_FOLDER}"

pm.run(geniml_cmd, universe_target_file)


# AFTER UNIVERSE IS CREATED, ASSESS 
prefix = f"{UNIVERSE}_{SCORE}_{sample_name}"
assess_target = prefix+"_data.csv"
assess_command = f"geniml assess-universe --overlap --distance --distance-universe-to-file --universe {universe_target_file} --raw-data-folder {INPUT_DIRECTORY} --folder-out {STATS_OUTPUT} --save-to-file --file-list {FILE_LIST} --pref {prefix}"

pm.run(assess_command, assess_target)

pm.stop_pipeline()