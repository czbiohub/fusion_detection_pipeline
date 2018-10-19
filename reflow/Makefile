# Makefile
# authors: Lincoln Harris
# date: 10.19.18

# test_gatk -- run GATK reflow pipeline for a single cell. 
#		need to specify full s3 paths here
test:
	reflow run fusionDetectionReflow.rf -read1_fq=s3://darmanis-group/singlecell_lungadeno/nonImmune_fastqs_9.27/180226/C3_1001000403/C3_1001000403_S123_R1_001.fastq.gz -read2_fq=s3://darmanis-group/singlecell_lungadeno/nonImmune_fastqs_9.27/180226/C3_1001000403/C3_1001000403_S123_R2_001.fastq.gz -sample_id=C3_1001000403 -output_dir=s3://darmanis-group/singlecell_lungadeno/nonImmune_fastqs_9.27/180226/C3_1001000403/fusionPipelineOut/

