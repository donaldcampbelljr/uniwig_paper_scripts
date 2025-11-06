# gtars-uniwig scripts for scoring work

This project contains PEPs and pipelines to explore the use of the scoring flag in gtars-uniwig to create `bigwig` files with and without scoring used for accumulations.

Scored and No-Scored `bw` files are then fed into geniml's universe creation module. Various universes are then compared against the source files (the one used to create the `bw` files) to determine recall of genomic regions.

IGV is helpful in visually assessing `bw` and `universes`.
