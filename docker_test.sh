#####################################################################
#####################################################################
# script: docker_test.sh
# author: Lincoln 
# date: 8.15.18
#
# Lets try to run this guy from Docker...probably a better idea than
# a straight up install. 
#####################################################################
#####################################################################
#!/bin/bash

docker run -v `pwd`:/data --rm trinityctat/ctatfusion /usr/local/src/STAR-Fusion/STAR-Fusion --left_fq ./testCells_raw/A10_B000863/A10_B000863_S250_R1_001.fastq --right_fq ./testCells_raw/A10_B000863/A10_B000863_S250_R2_001.fastq --genome_lib_dir ./STAR-Fusion-v1.4.0/GRCh37_v19_CTAT_lib_Feb092018/ctat_genome_lib_build_dir/ -O ./test --FusionInspector validate --examine_coding_effect --denovo_reconstruct --CPU 4

#####################################################################
#####################################################################
