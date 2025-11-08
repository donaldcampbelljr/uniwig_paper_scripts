# gtars-uniwig scripts for scoring work

This project contains PEPs and pipelines to explore the use of the scoring flag in gtars-uniwig to create `bigwig` files with and without scoring used for accumulations.

Scored and No-Scored `bw` files are then fed into geniml's universe creation module. Various universes are then compared against the source files (the one used to create the `bw` files) to determine recall of genomic regions.

IGV is helpful in visually assessing `bw` and `universes`.


Initial results are located on HPC for 3 different sets of files:
`/project/shefflab/brickyard/results_pipeline/gtars_uniwig`

1. ATACseq ~ 500 files
2. lymphoblasotid ~ 400 files
3. scatlas2 samples ~ 358 files

For 1, there are many more files that could be used for this work; I did a random sampling of 500 files to keep output sizes low for proof of concept experimentation.

## Example running these pipelines

### ATACSEQ 500 27aug2025

`export RESULTS=/project/shefflab/brickyard/results_pipeline/gtars_uniwig/experiment_ATACseq_500`

`export CHROMSIZESPATH=/home/zzz3fh/files_for_gtars_uniwig/hg38.chrom.sizes`

`export GTARSPATH=/home/zzz3fh/code/gtars/gtars/target/release/gtars`

#### Create bigwig files
`looper run -c .looper_uniwig.yaml --package slurm --compute PARTITION=standard time='01-00:00:00' cores='12' mem='64000' -k 2 -d`

#### Create universes using the above bigwig files
`looper run -c .looper_parallel_universe.yaml --package slurm --compute PARTITION=standard time='01-00:00:00' cores='12' mem='64000' -k 16 -d`

Once these two pipelines are finished, you can take the `stats.py` script and point it to the `stats_output` directory to create figures:
`/project/shefflab/brickyard/results_pipeline/gtars_uniwig/experiment_ATACseq_500/stats_output`
