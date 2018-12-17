# Makefile
# authors: Lincoln Harris
# date: 10.19.18

# test -- run GATK reflow pipeline for a single cell. 
#		need to specify full s3 paths here
test:
	reflow run fusionDetectionReflow.rf -read1_fq=s3://darmanis-group/singlecell_lungadeno/non_immune/nonImmune_fastqs_9.27/170125/A10_1001000293/A10_1001000293_R1_001.fastq.gz -read2_fq=s3://darmanis-group/singlecell_lungadeno/non_immune/nonImmune_fastqs_9.27/170125/A10_1001000293/A10_1001000293_R2_001.fastq.gz -sample_id=A10_1001000293 -output_dir=s3://darmanis-group/singlecell_lungadeno/non_immune/nonImmune_fastqs_9.27/STAR-fus_out/A10_1001000293/
